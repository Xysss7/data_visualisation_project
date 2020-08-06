from IPython.core.display import display, HTML
from IPython.display import Javascript
from matplotlib import cm
from .data_validation import *
import json


def check_data(ver, ele, point):
    if check_vertices(ver) == False: return False
    if check_faces(ele) == False: return False
    if check_data_color(ele, point) == False: return False


def display_data_elements():
    html_code_visual_elements = """
    <style> canvas { width: 50%; height: 50% }</style>
    <div class="output_area">
        <div id="mydiv_el" style="width:50%;height:50%">
        </div>
        <div id="outputnew">
        </div>
    </div>
    <script type="module">
        // initial set up
        import * as THREE from 'https://unpkg.com/three@0.118.3/build/three.module.js';
        
        import { OrbitControls } from 'https://unpkg.com/three@0.118.3/examples/jsm/controls/OrbitControls.js';

        var renderWindowContainer = document.getElementById("mydiv_el");
        var scene = new THREE.Scene();
        var camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
        var renderer = new THREE.WebGLRenderer();
        renderer.setSize(400, 400);
        renderWindowContainer.appendChild(renderer.domElement);
        camera.lookAt(new THREE.Vector3(0,0,0));
        camera.position.set( 0, 0, 1 );

        var controls = new OrbitControls( camera, renderer.domElement );
        var geometry = new THREE.Geometry();
        var vertices = document.triangleDataEle.vertices;    
        var faces = document.triangleDataEle.faces;    
        var facecolors = document.triangleDataEle.colors;    

        var i = 0;
        for (i = 0; i < vertices.length; i += 3) { 
            geometry.vertices.push(new THREE.Vector3(vertices[i], vertices[i+1], vertices[i+2]));
        }
        console.log(
            document.triangleDataEle,
            faces
        );
        var colors = new Array();
        for (i = 0; i < facecolors.length; i++) { 
            colors[i] = new THREE.Color( facecolors[i][0], facecolors[i][1], facecolors[i][2] );
        }
        console.log('colors readed');
        var j = 0;
        for (i = 0; i < faces.length; i += 3) { 
            geometry.faces.push(new THREE.Face3( faces[i], faces[i+1], faces[i+2] ));
            geometry.faces[j].color.set( colors[j] );
            j = j+1;
        }
        console.log('colors applied');

        geometry.computeFaceNormals();
        var parameters = {
            vertexColors: THREE.FaceColors,
            side: THREE.DoubleSide
        };
        var material = new THREE.MeshBasicMaterial(parameters);
        var triangles = new THREE.Mesh(geometry, material); 
        triangles.translateX(-0.5);;
        triangles.translateY(-0.5);;

        scene.add(triangles);
        camera.position.z = 2;
        animate();
        controls.addEventListener( 'change', render );
        renderWindowContainer.id = "usedid";

        function render() {
            renderer.render( scene, camera );
        }
        function animate(){
            requestAnimationFrame( animate );
            controls.update();
            renderer.render( scene, camera );
        }
    </script>
    """
    display(HTML(html_code_visual_elements))


def passdata_ele(ver, ele, eledata):
    check_result = check_data(ver, ele, eledata)
    if check_result == False:
        return False
    colord = [ cm.jet(x) for x in eledata ]
    js_code = """
    document.triangleDataEle = %s; 
    console.log(document.triangleDataEle);
    """ % json.dumps({'vertices': ver, 'faces': ele, 'colors': colord})
    print("Passing the data...")
    return Javascript(js_code)


def visualization_ele(ver, ele, eledata):
    if passdata_ele(ver, ele, eledata) == False:
        return
    print("Display:")
    display_data_elements()


if __name__ == "__main__":
    vertices = [0, 0, 0,
                1, 0, 0,
                1, 1, 0,
                0, 1, 0]
    faces = [0, 1, 2,
             0, 2, 3]
    colors = [0.0, 1.0]
    visualization_ele(vertices, faces, colors)