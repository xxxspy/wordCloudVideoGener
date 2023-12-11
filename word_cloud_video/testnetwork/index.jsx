const { useRef, useCallback, useEffect  } = React;
        import { UnrealBloomPass } from '//unpkg.com/three/examples/jsm/postprocessing/UnrealBloomPass.js';
      fetch('./data.json').then(res => res.json()).then(data => {
        const FocusGraph = () => {
          const fgRef = useRef();


          useEffect(() => {
            const bloomPass = new UnrealBloomPass();
            bloomPass.strength = 4;
            bloomPass.radius = 1;
            bloomPass.threshold = 0;
            fgRef.current.postProcessingComposer().addPass(bloomPass);
            setInterval(()=>{
                fgRef.current.cameraPosition
            })

          }, []);

          const handleClick = useCallback(node => {
            // Aim at node from outside it
            const distance = 160;
            const distRatio = 1 + distance/Math.hypot(node.x, node.y, node.z);
  
            fgRef.current.cameraPosition(
              { x: node.x * distRatio, y: node.y * distRatio, z: node.z * distRatio }, // new position
              node, // lookAt ({ x, y, z })
              1000  // ms transition duration
            );
          }, [fgRef]);
  
          return <ForceGraph3D
            backgroundColor="#000003"
            ref={fgRef}
            graphData={data}
            nodeLabel="label"
            nodeAutoColorBy="group"
            onNodeClick={handleClick}
            linkDirectionalArrowLength={3.5}
            linkDirectionalArrowRelPos={1}
            linkCurvature=" "
            nodeThreeObject={node => {
                const sprite = new SpriteText(node.label);
                sprite.color = node.color;
                sprite.textHeight = 8;
                return sprite;
            }}
          />;
        };
  
        ReactDOM.render(
          <FocusGraph />,
          document.getElementById('graph')
        );
      });