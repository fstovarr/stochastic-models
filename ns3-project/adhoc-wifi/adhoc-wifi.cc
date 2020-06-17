#include "ns3/command-line.h"
#include "ns3/core-module.h"
#include "ns3/mobility-module.h"
#include "ns3/log.h"
#include "ns3/yans-wifi-helper.h"
#include "ns3/internet-stack-helper.h"
#include "ns3/ipv4-address-helper.h"
#include "ns3/config.h"
#include "ns3/applications-module.h"
#include "ns3/aodv-module.h"
#include "ns3/v4ping-helper.h"
#include "ns3/internet-apps-module.h"
#include "ns3/internet-module.h"
#include "ns3/opengym-module.h"
#include "ns3/node-list.h"
#include "ns3/wifi-net-device.h"
#include <math.h>

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("adhoc-wifi");

// Auxiliary variables to get some parameters
float rcvPackages = 0.0, lastRecvPackages = 0.0;
double accRtt = 0.0, lastAccRtt = 0.0;

// Available power levels for the wifi manager
double txPowerLevels = 50;

// Variable that control the seconds in which the nodes will be without movement
uint32_t secondsPaused = ((int) (log2(txPowerLevels) + 0.5)) + 1;

// The observation space is a tuple
Ptr<OpenGymSpace> GetObservationSpace() 
{
  Ptr<OpenGymTupleSpace> space = CreateObject<OpenGymTupleSpace> ();
  NS_LOG_UNCOND("Observation space: " << space);
  return space;
}

// The action space is the available power levels
Ptr<OpenGymSpace> GetActionSpace() 
{
  Ptr<OpenGymDiscreteSpace> space = CreateObject<OpenGymDiscreteSpace> (txPowerLevels);
  NS_LOG_UNCOND("Action space: " << space);
  return space;
}

// The ping's RTT and received packages, and a vector with all positions of nodes are the observation for the agents 
Ptr<OpenGymDataContainer> GetObservation() 
{
  Ptr<OpenGymTupleContainer> container = CreateObject<OpenGymTupleContainer> ();

  Ptr< OpenGymBoxContainer<double> > rttContainer = CreateObject< OpenGymBoxContainer<double> > (); 
  rttContainer->AddValue (accRtt);

  Ptr< OpenGymBoxContainer<uint32_t> > packagesContainer = CreateObject< OpenGymBoxContainer<uint32_t> > (); 
  packagesContainer->AddValue (rcvPackages);

  Ptr<OpenGymTupleContainer> positionsContainer = CreateObject<OpenGymTupleContainer> ();

  double nodeNum = (double) NodeList::GetNNodes ();
  std::vector<double> nodesShape = {nodeNum, };

  for (NodeList::Iterator i = NodeList::Begin (); i != NodeList::End (); ++i) {
    Ptr<Node> node = *i;
    Ptr<MobilityModel> mobility = node->GetObject<MobilityModel> ();
    if (!mobility) continue;

    Vector pos = mobility->GetPosition ();

    Ptr< OpenGymBoxContainer<double> > nodePosition = CreateObject< OpenGymBoxContainer<double> > (); 
    nodePosition->AddValue (pos.x);
    nodePosition->AddValue (pos.y);
    
    positionsContainer->Add (nodePosition);
  }

  container->Add (rttContainer);
  container->Add (packagesContainer);
  container->Add (positionsContainer);

  return container;
}

// If there are new packages in this step, the reward will be 1, otherwise 0
float GetReward() 
{
  return ((rcvPackages - lastRecvPackages) >= 1) ? 1 : 0;
}

bool GetGameOver() 
{
  return false;
}

std::string GetExtraInfo() 
{
  return "";
}

// The power level of the wifi manager of each node is changed by the action choosen by the agent
bool ExecuteActions(Ptr<OpenGymDataContainer> action) 
{
  Ptr<OpenGymDiscreteContainer> discrete = DynamicCast<OpenGymDiscreteContainer>(action);
  uint32_t gain = discrete->GetValue();

  NS_LOG_UNCOND ("Action: " << gain);

  Config::Set("/NodeList/*/DeviceList/*/$ns3::WifiNetDevice/RemoteStationManager/$ns3::ConstantRateWifiManager/DefaultTxPowerLevel", UintegerValue (gain));

  return true;
}

void ScheduleNextStateRead(double envStepTime, Ptr<OpenGymInterface> openGymInterface)
{
  Simulator::Schedule (Seconds(envStepTime), &ScheduleNextStateRead, envStepTime, openGymInterface);
  openGymInterface->NotifyCurrentState();
  lastAccRtt = accRtt;
  lastRecvPackages = rcvPackages;
  accRtt = 0.0;
}

static void PingRtt (std::string context, Time rtt) 
{
  accRtt += rtt.GetNanoSeconds ();
  rcvPackages++;
}

void ResumeNodeMobility(double envStepTime);

void PauseNodeMobility(double envStepTime) 
{
  Config::Set("/NodeList/*/$ns3::MobilityModel/$ns3::RandomWalk2dMobilityModel/Speed", StringValue("ns3::ConstantRandomVariable[Constant=0]"));
  Simulator::Schedule (Seconds(secondsPaused * envStepTime), &ResumeNodeMobility, envStepTime);
}

void ResumeNodeMobility(double envStepTime) 
{
  Config::Set("/NodeList/*/$ns3::MobilityModel/$ns3::RandomWalk2dMobilityModel/Speed", StringValue("ns3::UniformRandomVariable[Min=0|Max=0.15]"));
  Simulator::Schedule (MilliSeconds((envStepTime * 1000) / 2), &PauseNodeMobility, envStepTime);
}

int main(int argc, char *argv[]) 
{
  uint32_t nNodes = 25;            

  uint32_t referenceLoss = 46.6777;
  double txPowerStart = 0.0;
  double txPowerEnd = 50.0;
  
  uint32_t simSeed = 1;
  double simulationTime = 20;
  double envStepTime = 5;         
  uint32_t openGymPort = 5555;

  CommandLine cmd;
  cmd.AddValue ("nNodes", "Number of nodes in the network", nNodes);
  
  cmd.AddValue ("stepTime", "Step time fot OpenGym env. Default: 1", envStepTime);
  cmd.AddValue ("txStart", "Start of power transmission. Default: 0", txPowerStart);
  cmd.AddValue ("txEnd", "End of power transmission. Default: 50", txPowerEnd);
  cmd.AddValue ("txLevels", "Power levels. Default: 51", txPowerLevels);

  // NS3 environment variables
  cmd.AddValue ("openGymPort", "Port number for OpenGym env. Default: 5555", openGymPort);
  cmd.AddValue ("simSeed", "Seed for random generator. Default: 1", simSeed);
  cmd.AddValue ("simTime", "Simulation time in seconds. Default: 10s", simulationTime);

  cmd.Parse (argc, argv);

  NS_LOG_UNCOND("Nodes: " << nNodes);
  NS_LOG_UNCOND("Simulation time: " << simulationTime);
  NS_LOG_UNCOND("Tx power: (" << txPowerStart << ", " << txPowerEnd << ")");
  
  NS_LOG_UNCOND("Ns3Env parameters:");
  NS_LOG_UNCOND("--simulationTime: " << simulationTime);
  NS_LOG_UNCOND("--openGymPort: " << openGymPort);
  NS_LOG_UNCOND("--envStepTime: " << envStepTime);
  NS_LOG_UNCOND("--seed: " << simSeed);

  RngSeedManager::SetSeed (1);
  RngSeedManager::SetRun (simSeed);

  NodeContainer nodes;
  nodes.Create (nNodes);

  // Each node will have a random position with a max radio of 0.5 meters
  MobilityHelper mobility;
  mobility.SetPositionAllocator (
    "ns3::RandomDiscPositionAllocator",
    "X", StringValue ("2.5"),
    "Y", StringValue ("2.5"),
    "Theta", StringValue ("ns3::UniformRandomVariable[Min=0|Max=6.2830]"), // Ángulo
    "Rho", StringValue ("ns3::UniformRandomVariable[Min=0|Max=0.5]") // Radio
  );

  // Each node will move from its start position in a bounded box of 5x5
  // The nodes start stopped (Speed 0)
  mobility.SetMobilityModel (
    "ns3::RandomWalk2dMobilityModel",
    "Mode", StringValue ("Time"),
    "Speed", StringValue ("ns3::ConstantRandomVariable[Constant=0]"),
    "Bounds", StringValue ("0|5|0|5"),
    "Time", TimeValue (MilliSeconds(envStepTime * 1000))
  );

  mobility.Install(nodes);

  // WiFi configuration with a loss propagation that depends on the distance to be more realistic 
  YansWifiChannelHelper channel = YansWifiChannelHelper::Default ();
  channel.SetPropagationDelay ("ns3::ConstantSpeedPropagationDelayModel");
  channel.AddPropagationLoss (
    "ns3::LogDistancePropagationLossModel", 
    "ReferenceLoss", DoubleValue (referenceLoss),
    "Exponent", DoubleValue (1)
  );

  // WiFi Physical layer
  YansWifiPhyHelper phy = YansWifiPhyHelper::Default ();
  phy.SetChannel (channel.Create ());
  phy.EnablePcapAll (std::string ("aodv"));

  // Definition of minimum and maximum transmission power and its different levels
  phy.Set ("TxPowerStart", DoubleValue (txPowerStart));     
  phy.Set ("TxPowerEnd", DoubleValue (txPowerEnd));     
  phy.Set ("TxPowerLevels", UintegerValue (txPowerLevels));

  // Adhoc mac layer
  WifiMacHelper mac;
  mac.SetType("ns3::AdhocWifiMac");

  // Remote station configuration with the first level as default
  WifiHelper wifi;
  wifi.SetRemoteStationManager (
    "ns3::ConstantRateWifiManager", 
    "DefaultTxPowerLevel", UintegerValue (1)
  );
  
  NetDeviceContainer devices;
  devices = wifi.Install(phy, mac, nodes);

  // Set the Adhoc On-Demand Distance Vector routing
  AodvHelper aodv;
  InternetStackHelper internet;
  internet.SetRoutingHelper (aodv);
  internet.Install (nodes);

  Ipv4AddressHelper ipv4;
  NS_LOG_INFO ("Assign IP Addresses.");
  ipv4.SetBase ("10.1.1.0", "255.255.255.0");
  Ipv4InterfaceContainer interfaces = ipv4.Assign (devices);

  // Ping from first to last node
  V4PingHelper ping (interfaces.GetAddress (nNodes - 1));
  ping.SetAttribute ("Interval", TimeValue (MilliSeconds (envStepTime * 1000)));
  ping.SetAttribute ("Verbose", BooleanValue (true));
  ping.SetAttribute ("Size", UintegerValue (1024));

  ApplicationContainer p = ping.Install (nodes.Get (0));
  p.Start (Seconds (0));
  p.Stop (Seconds (simulationTime));

  // OnOff traffic
  OnOffHelper onOffHelper ("ns3::TcpSocketFactory", interfaces.GetAddress (nNodes - 2));
  onOffHelper.SetAttribute ("OnTime", StringValue ("ns3::ConstantRandomVariable[Constant=10]"));
  onOffHelper.SetAttribute ("OffTime", StringValue ("ns3::ConstantRandomVariable[Constant=10]"));
  onOffHelper.SetAttribute ("DataRate", StringValue ("2Mbps"));
  onOffHelper.SetAttribute ("PacketSize", UintegerValue(1280));

  ApplicationContainer oop = onOffHelper.Install (nodes.Get (2));
  oop.Start (Seconds (0));
  oop.Stop (Seconds (simulationTime));

  // Connect a callback with to get the ping results
  Config::Connect ("/NodeList/" + std::to_string(0) + "/ApplicationList/*/$ns3::V4Ping/Rtt", MakeCallback (&PingRtt));

  // Opengym Environment
  Ptr<OpenGymInterface> openGymInterface = CreateObject<OpenGymInterface> (openGymPort);
  openGymInterface->SetGetActionSpaceCb( MakeCallback (&GetActionSpace) );
  openGymInterface->SetGetObservationSpaceCb( MakeCallback (&GetObservationSpace) );
  openGymInterface->SetGetGameOverCb( MakeCallback (&GetGameOver) );
  openGymInterface->SetGetObservationCb( MakeCallback (&GetObservation) );
  openGymInterface->SetGetRewardCb( MakeCallback (&GetReward) );
  openGymInterface->SetGetExtraInfoCb( MakeCallback (&GetExtraInfo) );
  openGymInterface->SetExecuteActionsCb( MakeCallback (&ExecuteActions) );

  // Pause all nodes at the start
  Simulator::Schedule (Seconds(0.0), &PauseNodeMobility, envStepTime);
  Simulator::Schedule (Seconds(0.0), &ScheduleNextStateRead, envStepTime, openGymInterface);

  Simulator::Stop (Seconds (simulationTime));
  Simulator::Run ();

  std::cout << (accRtt / rcvPackages) << " - " << rcvPackages << " (" << ((double) rcvPackages / (simulationTime*10)) * envStepTime * 1000 << "%)\n";
  
  openGymInterface->NotifySimulationEnd();
  Simulator::Destroy ();

  return 0;
}
