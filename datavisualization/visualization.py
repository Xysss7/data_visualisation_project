from IPython.core.display import display, HTML
from IPython.display import Javascript
from matplotlib import cm
from .data_validation import *
import json


def check_data(ver, ele, point):
    if check_vertices(ver) == False: return False
    if check_faces(ele) == False: return False
    if check_data_color(ver, point) == False: return False


def display_data():
    html_code_visual = """
    <style> canvas { width: 50%; height: 50% }</style>
    <div class="output_area">
        <div id="mydiv_op" style="width:50%;height:50%">
        </div>
        <div id="outputnew">
        </div>
    </div>
    <script type="module">
        // initial resource import
        import * as THREE from 'https://unpkg.com/three@0.118.3/build/three.module.js';
        import { OrbitControls } from 'https://unpkg.com/three@0.118.3/examples/jsm/controls/OrbitControls.js';

        // standard global variables
        var renderWindowContainer = document.getElementById("mydiv_op");
        var scene = new THREE.Scene();
        var camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
        var renderer = new THREE.WebGLRenderer();
        
        // canvas initial set up
        renderer.setSize(500, 500);
        renderWindowContainer.appendChild(renderer.domElement);
        camera.lookAt(new THREE.Vector3(0,0,0));
        camera.position.set( 0, 0, 1 );

        // other global variables
        var controls = new OrbitControls( camera, renderer.domElement );
        var geometry = new THREE.Geometry();
        var raycaster, mouse = { x : 0, y : 0 };

        // get scientific data from document.json that need to be visualized
        var faces = document.triangleDataSet.faces;    
        var data = document.triangleDataSet.pointdata;    
        var vertices = document.triangleDataSet.vertices;
        
        init()        
        animate();
        controls.addEventListener( 'change', render );
        renderWindowContainer.id = "usedid";  // avoid replicate use of the same div
        raycaster = new THREE.Raycaster();
        renderer.domElement.addEventListener( 'click', raycast, false );
        
        function init() {
            var i = 0;
            for (i = 0; i < vertices.length; i += 3) { 
                geometry.vertices.push(new THREE.Vector3(vertices[i], vertices[i+1], vertices[i+2]));
            }        
            var colors = new Array();
            for (i = 0; i < data.length; i++) { 
                colors[i] = new THREE.Color(data[i][0], data[i][1], data[i][2]);
            }
            var j = 0;
            for (i = 0; i < faces.length; i += 3) { 
                geometry.faces.push(new THREE.Face3(faces[i], faces[i+1], faces[i+2]));
                geometry.faces[j].vertexColors.push( colors[faces[i]], colors[faces[i+1]], colors[faces[i+2]] );
                j = j+1;
            }
            geometry.computeFaceNormals();
            var parameters = {
                vertexColors: THREE.VertexColors,
                side: THREE.DoubleSide
            };
            var material = new THREE.MeshBasicMaterial(parameters);
            var triangles = new THREE.Mesh(geometry, material); 
            //triangles.translateX(-0.5);;
            //triangles.translateY(-0.5);;

            scene.add(triangles);
            camera.position.z = 2;
        }
        
        function render() {
            renderer.render( scene, camera );
        }
        
        // allow the frame to be animated
        function animate(){
            requestAnimationFrame( animate );
            controls.update();
            renderer.render( scene, camera );
        }
        
        // Obtain the object intersected by the ray 
        // and console.log information including
        // picked element index
        // picked element vertices coordinates
        function raycast ( e ) {

            //1. sets the mouse position with a coordinate system where the center
            //   of the canvas is the origin
            let canvasBounds = renderer.getContext().canvas.getBoundingClientRect();
            mouse.x = ( ( event.clientX - canvasBounds.left ) / ( canvasBounds.right - canvasBounds.left ) ) * 2 - 1;
            mouse.y = - ( ( event.clientY - canvasBounds.top ) / ( canvasBounds.bottom - canvasBounds.top) ) * 2 + 1;
            const mpoint = [mouse.x, mouse.y, 0.0];
            console.log(`Pick at: ${mpoint}`); 
            
            //2. set the picking ray from the camera position and mouse coordinates
            raycaster.setFromCamera( mouse, camera );    

            //3. compute intersections
            var intersects = raycaster.intersectObjects( scene.children );
            
            if (intersects.length == 0) {
                console.log( "No elements picked" ); 
            } else {
                console.log( 'Picked element: ', intersects[ 0 ] ); 
                console.log( 'Picked element index: ', intersects[ 0 ].faceIndex );
                console.log( 'Picked point: ', intersects[ 0 ].point );
                var intface = intersects[ 0 ].face;
                var a = [ vertices[3*intface.a], vertices[3*intface.a+1], vertices[3*intface.a+2] ];
                var b = [ vertices[3*intface.b], vertices[3*intface.b+1], vertices[3*intface.b+2] ];
                var c = [ vertices[3*intface.c], vertices[3*intface.c+1], vertices[3*intface.c+2] ];
                console.log( 'Picked element vertices coordinates: ', a, b, c );
                // change the color of the closest face.
                intface.color.setRGB( 0.8 * Math.random() + 0.2, 0, 0 ); 
                intersects[ 0 ].object.geometry.colorsNeedUpdate = true;
            }
            renderer.render( scene, camera );
            
            // if want to get all objects clicked and objects behind the clicked elements 
            // (keep for functions in future)
            /*
            for ( var i = 0; i < intersects.length; i++ ) {
                console.log( intersects[ i ] ); 
                console.log( intersects[ i ].point ); 
            }
            */
        }
    </script>
    """
    display(HTML(html_code_visual))


def passdata(ver, ele, point):
    check_result = check_data(ver, ele, point)
    if check_result == False:
        return False
    colord = [ cm.jet(x) for x in point ]
    #div_name = ranstr(4)
    js_code = """
    document.triangleDataSet = %s; 
    console.log(document.triangleDataSet);
    """ % json.dumps({'vertices': ver, 'faces': ele, 'pointdata': colord})
    print("Passing the data...")
    return Javascript(js_code)


def visualization(ver, ele, pointdata):
    if passdata(ver, ele, pointdata) == False: 
        return
    print("Display:")
    display_data()


if __name__ == "__main__":
    vertices = [0, 0, 0,
                1, 0, 0,
                1, 1, 0,
                0, 1, 0]
    faces = [0, 1, 2,
             0, 2, 3]
    point_data = [0.0, 1.0, 2.3, .5]
    visualization(vertices, faces, point_data)