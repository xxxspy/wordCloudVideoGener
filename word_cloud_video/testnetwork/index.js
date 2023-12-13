const N = 50
const Graph = ForceGraph3D()
Graph.cooldownTime(Infinity)
.d3AlphaDecay(0)
.d3VelocityDecay(0)

// Deactivate existing forces
.d3Force('center', null)
.d3Force('charge', null)


(document.getElementById('3d-graph'))
  .jsonUrl('./data.json')
  .nodeAutoColorBy('group')
  .nodeThreeObject(node => {
    const sprite = new SpriteText(node.label);
    sprite.material.depthWrite = false; // make sprite background transparent
    sprite.color = node.color;
    sprite.textHeight = 4;
    return sprite;
  })
  .nodeVal('val')
  // .nodeVisibility(node=>{
  //   return (node.id <= currentNodeID)&(node.id>currentNodeID-10)
  // })
  .linkCurvature('curve')
  .onNodeClick(focusNodeGroup)
  // .d3Force('collide', d3.forceCollide(Graph.nodeRelSize()))



let currentGroupID;
let currentNodeID = -1;

let nodeIndex = -1;

Graph.d3Force('line', ()=>{
  const { nodes, links } = Graph.graphData();
  nodes.forEach(node=>{
    if(node.group == currentGroupID){
      node.vy = -0.1 * node.y;
      node.vz = -0.1 * node.z;
    }
  })
})
.d3Force('box', () => {
  const CUBE_HALF_SIDE = Graph.nodeRelSize() * N * 0.5;
  const { nodes, links } = Graph.graphData();
  nodes.forEach(node => {
    const x = node.x || 0, y = node.y || 0, z = node.z || 0;
    // bounce on box walls
    if (Math.abs(x) > CUBE_HALF_SIDE) { node.vx *= -1; }
    if (Math.abs(y) > CUBE_HALF_SIDE) { node.vy *= -1; }
    if (Math.abs(z) > CUBE_HALF_SIDE) { node.vz *= -1; }
  })
})

  setInterval(()=>{
    nodeIndex += 1;
    const { nodes, links } = Graph.graphData();
    if(nodes[nodeIndex].group != currentGroupID){
      currentGroupID = nodes[nodeIndex].group;
    }
    
  }, 1000)


function focusNodeGroup(currentNode){
  currentNodeID = currentNode.id
  Graph.refresh()
  const { nodes, links } = Graph.graphData();

  // currentNode.nodeVisibility(1)
  if(currentGroupID!=undefined){
    if(currentGroupID==currentNode.group){
      console.log('pass....')
      return
    }
  }
  currentGroupID = currentNode.group
  const distance = 120;
  
  
  const groupNodes = nodes.filter(node=>node.group==currentNode.group)
  let x = 0;
  let y = 0;
  let z = 0;
  groupNodes.forEach(node=>{
    x += node.x;
    y += node.y;
    z += node.z;
  })
  group = {x: x/groupNodes.length, y: y/groupNodes.length, z: z/groupNodes.length}

  const distRatio = 1 + distance/Math.hypot(group.x, group.y, group.z);
  const newPos = group.x || group.y || group.z
    ? { x: group.x * distRatio, y: group.y * distRatio, z: group.z * distRatio }
    : { x: 0, y: 0, z: distance }; // special case if group is in (0,0,0)
  console.log('change position')
  console.log(newPos)
  Graph.cameraPosition(
    newPos, // new position
    group, // lookAt ({ x, y, z })
    3000  // ms transition duration
  );
}

// let currentNodeNum = -1
// setInterval(()=>{
//     currentNodeNum += 1
//     const { nodes, links } = Graph.graphData();
//     if(currentNodeNum==nodes.length){return}
//     focusNodeGroup(nodes[currentNodeNum])
//     // console.log('------------------')
// }, 1000)

// Spread nodes a little wider
// Graph.d3Force('charge').strength(-300);
// Graph.d3Force('center').strength(-0);
let defaultStrength = Graph.d3Force('link').strength()

// Graph.d3Force('link').strength(0)
