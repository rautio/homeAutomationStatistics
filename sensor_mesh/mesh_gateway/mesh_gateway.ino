//************************************************************
// this is a simple example that uses the painlessMesh library
//
// 1. sends a silly message to every node on the mesh at a random time betweew 1 and 5 seconds
// 2. prints anything it recieves to Serial.print
//
//
//************************************************************
#include <painlessMesh.h>
#include <painlessMeshSync.h>
#include <painlessScheduler.h>



#define   MESH_PREFIX     "HakalaSensorNode"
#define   MESH_PASSWORD   "password"
#define   MESH_PORT       5555


enum meshNodeType {
  MESH_GATEWAY = 1,
  MESH_DHT_NODE= 2,
  MESH_UNKNOWN = 0
};

meshNodeType node_type = MESH_UNKNOWN;
painlessMesh  mesh;





void receivedCallback( uint32_t from, String &msg ) {
  Serial.printf(";R;%u;msg;%s", from, msg.c_str());
}

void newConnectionCallback(uint32_t nodeId) {
    //Serial.printf("--> startHere: New Connection, nodeId = %u\n", nodeId);
}

void changedConnectionCallback() {
    //Serial.printf("Changed connections %s\n",mesh.subConnectionJson().c_str());
}

void nodeTimeAdjustedCallback(int32_t offset) {
    //Serial.printf("Adjusted time %u. Offset = %d\n", mesh.getNodeTime(),offset);
}

void setup() {
  Serial.begin(9600);

//mesh.setDebugMsgTypes( ERROR | MESH_STATUS | CONNECTION | SYNC | COMMUNICATION | GENERAL | MSG_TYPES | REMOTE ); // all types on
  mesh.setDebugMsgTypes( ERROR | STARTUP );  // set before init() so that you can see startup messages

  mesh.init( MESH_PREFIX, MESH_PASSWORD, MESH_PORT );
  mesh.onNodeTimeAdjusted(&nodeTimeAdjustedCallback);

  node_type = MESH_GATEWAY;  

  mesh.onReceive(&receivedCallback);
  mesh.onNewConnection(&newConnectionCallback);
  mesh.onChangedConnections(&changedConnectionCallback);

  Serial.printf("Setup Done");

}

void loop() {
  mesh.update();
}
