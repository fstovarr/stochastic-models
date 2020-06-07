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

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("MANET network");

float rcvPackages = 0.0, lastRecvPackages = 0.0;
double accRtt = 0.0, lastAccRtt = 0.0;

Ptr<OpenGymSpace> GetObservationSpace() 
{
  Ptr<OpenGymTupleSpace> space = CreateObject<OpenGymTupleSpace> ();
  NS_LOG_UNCOND("Observation space: " << space);
  return space;
}

Ptr<OpenGymSpace> GetActionSpace() 
{
  Ptr<OpenGymDiscreteSpace> space = CreateObject<OpenGymDiscreteSpace> (200);
  NS_LOG_UNCOND("Action space: " << space);
  return space;
}

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

  NS_LOG_UNCOND("Observation sent");
  return container;
}

float GetReward() 
{
  return rcvPackages - lastRecvPackages;
}

bool GetGameOver() 
{
  return false;
}

std::string GetExtraInfo() 
{
  return "";
}

bool ExecuteActions(Ptr<OpenGymDataContainer> action) 
{
  Ptr<OpenGymDiscreteContainer> discrete = DynamicCast<OpenGymDiscreteContainer>(action);
  uint32_t gain = discrete->GetValue();
  
  Config::Set("/NodeList/*/DeviceList/*/$ns3::WifiNetDevice/Phy/$ns3::YansWifiPhy/RxGain", DoubleValue((double) gain));
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

int main(int argc, char *argv[]) 
{
  uint32_t nNodes = 25;                     // 
  uint32_t httpServerNode = 1;              // 
  uint32_t simulationTime = 50;             // Seconds
  uint32_t seed = 1;                        // Simulation seed
  uint32_t referenceLoss = 46.6777;         // Simulation seed
  double rxGain = 0;                        // 
  uint32_t openGymPort = 5555;              // 
  double envStepTime = 1;                   // seconds, ns3gym env step time interval

  CommandLine cmd;
  cmd.AddValue ("nNodes", "Number of nodes in the network", nNodes);
  cmd.AddValue ("sNode", "Node with the HTTP server", httpServerNode);
  cmd.AddValue ("simTime", "Simulation time in seconds", simulationTime);
  cmd.AddValue ("phyGain", "RX Gain in physical layer", rxGain);
  cmd.AddValue ("refLoss", "Reference loss at reference distance (dB)", referenceLoss);
  cmd.AddValue ("openGymPort", "Port number for OpenGym env. Default: 5555", openGymPort);
  cmd.AddValue ("stepTime", "Step time fot OpenGym env. Default: 1", envStepTime);
  cmd.Parse (argc, argv);

  NS_LOG_UNCOND("Nodes: %u " << nNodes);
  NS_LOG_UNCOND("Simulation time: " << simulationTime);

  RngSeedManager::SetSeed (1);
  RngSeedManager::SetRun (seed);

  NodeContainer nodes;
  nodes.Create (nNodes);

  // Position and mobility
  MobilityHelper mobility;
  mobility.SetPositionAllocator (
    "ns3::RandomDiscPositionAllocator",
    "X", StringValue ("750.0"),
    "Y", StringValue ("750.0"),
    "Theta", StringValue ("ns3::UniformRandomVariable[Min=0|Max=6.2830]"), // Ángulo
    "Rho", StringValue ("ns3::UniformRandomVariable[Min=0|Max=5]") // Radio
  );

  mobility.SetMobilityModel (
    "ns3::RandomWalk2dMobilityModel",
    "Mode", StringValue ("Time"),
    "Time", StringValue ("1s"),
    "Speed", StringValue ("ns3::UniformRandomVariable[Min=0|Max=1]"),
    "Bounds", StringValue ("0|1500|0|1500")
  );
  mobility.Install(nodes);

  // WiFi config
  YansWifiChannelHelper channel = YansWifiChannelHelper::Default ();
  channel.SetPropagationDelay ("ns3::ConstantSpeedPropagationDelayModel");
  channel.AddPropagationLoss (
    "ns3::LogDistancePropagationLossModel", 
    "ReferenceLoss", DoubleValue (referenceLoss)
  );

  YansWifiPhyHelper phy = YansWifiPhyHelper::Default ();
  phy.Set ("RxGain", DoubleValue (rxGain) );
  phy.SetChannel (channel.Create ());
  phy.EnablePcapAll (std::string ("aodv"));

  WifiMacHelper mac;
  mac.SetType("ns3::AdhocWifiMac");

  WifiHelper wifi;
  // wifi.SetStandard (WIFI_PHY_STANDARD_80211g);
  
  NetDeviceContainer devices;
  devices = wifi.Install(phy, mac, nodes);

  AodvHelper aodv;
  InternetStackHelper internet;
  internet.SetRoutingHelper (aodv);
  internet.Install (nodes);

  Ipv4AddressHelper ipv4;
  NS_LOG_INFO ("Assign IP Addresses.");
  ipv4.SetBase ("10.1.1.0", "255.255.255.0");
  Ipv4InterfaceContainer interfaces = ipv4.Assign (devices);

  // Config::SetDefault ("ns3::Ipv4RawSocketImpl::Protocol", StringValue ("2"));

  // Ping from first to last node
  V4PingHelper ping (interfaces.GetAddress (nNodes - 1));
  ping.SetAttribute ("Verbose", BooleanValue (false));
  ApplicationContainer p = ping.Install (nodes.Get (0));
  p.Start (Seconds (0));
  p.Stop (Seconds (simulationTime));

  Config::Connect ("/NodeList/" + std::to_string(0) + "/ApplicationList/*/$ns3::V4Ping/Rtt", MakeCallback (&PingRtt));

  // OnOff traffic
  // OnOffHelper onOffHelper ("ns3::TcpSocketFactory", interfaces.GetAddress (nNodes - 1));
  // // onOffHelper.SetAttribute ("OnTime", StringValue ("ns3::ConstantRandomVariable[Constant=10]"));
  // // onOffHelper.SetAttribute ("OffTime", StringValue ("ns3::ConstantRandomVariable[Constant=10]"));
  // onOffHelper.SetAttribute ("DataRate", StringValue ("2Mbps"));
  // onOffHelper.SetAttribute ("PacketSize", UintegerValue(1280));

  // ApplicationContainer p = onOffHelper.Install (nodes.Get (0));
  // p.Start (Seconds (0));
  // p.Stop (Seconds (simulationTime));

  // PacketSinkHelper sink = PacketSinkHelper ("ns3::TcpSocketFactory", interfaces.GetAddress (nNodes - 1));
  // ApplicationContainer apps = sink.Install (nodes.Get (nNodes - 1));
  // apps.Start (Seconds (0.0));
  // apps.Stop (Seconds (simulationTime));

  // Config::ConnectWithoutContext ("/NodeList/*/ApplicationList/0/$ns3::PacketSink/Rx", 
  //                                MakeCallback (&SinkRx));

  // Config::ConnectWithoutContext ("/NodeList/*/ApplicationList/*/$ns3::OnOffApplication/Tx", MakeCallback (&OnOffRx));

  // for (uint32_t i = 0; i < nNodes; i++) {
  //   interfaces.GetAddress(i).Print(std::cout);
  //   printf("\n");
  // }

  // Opengym Environment
  Ptr<OpenGymInterface> openGymInterface = CreateObject<OpenGymInterface> (openGymPort);
  openGymInterface->SetGetActionSpaceCb( MakeCallback (&GetActionSpace) );
  openGymInterface->SetGetObservationSpaceCb( MakeCallback (&GetObservationSpace) );
  openGymInterface->SetGetGameOverCb( MakeCallback (&GetGameOver) );
  openGymInterface->SetGetObservationCb( MakeCallback (&GetObservation) );
  openGymInterface->SetGetRewardCb( MakeCallback (&GetReward) );
  openGymInterface->SetGetExtraInfoCb( MakeCallback (&GetExtraInfo) );
  openGymInterface->SetExecuteActionsCb( MakeCallback (&ExecuteActions) );

  Simulator::Schedule (Seconds(0.0), &ScheduleNextStateRead, envStepTime, openGymInterface);

  Simulator::Stop (Seconds (simulationTime));
  Simulator::Run ();

  std::cout << (accRtt / rcvPackages) << " - " << rcvPackages << " (" << ((double) rcvPackages / simulationTime) * 100 << "%)\n";
  
  openGymInterface->NotifySimulationEnd();
  Simulator::Destroy ();

  return 0;
}
