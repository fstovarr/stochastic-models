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

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("MANET network");

int main(int argc, char *argv[]) {
  uint32_t nNodes = 25;
  uint32_t httpServerNode = 1;
  uint32_t simulationTime = 20;             // Seconds
  uint32_t seed = 1;                        // Simulation seed
  uint32_t referenceLoss = 46.6777;         // Simulation seed
  double rxGain = 0;

  CommandLine cmd;
  cmd.AddValue ("nNodes", "Number of nodes in the network", nNodes);
  cmd.AddValue ("sNode", "Node with the HTTP server", httpServerNode);
  cmd.AddValue ("simTime", "Simulation time in seconds", simulationTime);
  cmd.AddValue ("phyGain", "RX Gain in physical layer", rxGain);
  cmd.AddValue ("refLoss", "Reference loss at reference distance (dB)", referenceLoss);
  cmd.Parse (argc, argv);

  NS_LOG_UNCOND("Nodes: %u " << nNodes);

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
    "ReferenceLoss", DoubleValue(referenceLoss)
  );

  YansWifiPhyHelper phy = YansWifiPhyHelper::Default ();
  phy.Set ("RxGain", DoubleValue (rxGain) );
  phy.SetChannel (channel.Create ());

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

  // Ping from first to last node
  V4PingHelper ping (interfaces.GetAddress (nNodes - 1));
  ping.SetAttribute ("Verbose", BooleanValue (true));

  ApplicationContainer p = ping.Install (nodes.Get (0));
  p.Start (Seconds (0));
  p.Stop (Seconds (simulationTime));

  // for (uint32_t i = 0; i < nNodes; i++) {
  //   interfaces.GetAddress(i).Print(std::cout);
  //   printf("\n");
  // }

  Simulator::Stop (Seconds (simulationTime));
  Simulator::Run ();
  Simulator::Destroy ();
  return 0;
}