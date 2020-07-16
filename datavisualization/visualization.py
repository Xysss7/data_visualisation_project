from IPython.core.display import display, HTML
from IPython.display import Javascript
from matplotlib import cm
import json


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
        // initial set up
        import * as THREE from 'https://unpkg.com/three@0.118.3/build/three.module.js';
        
        import { OrbitControls } from 'https://unpkg.com/three@0.118.3/examples/jsm/controls/OrbitControls.js';

        var renderWindowContainer = document.getElementById("mydiv_op");
        var scene = new THREE.Scene();
        var camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
        var renderer = new THREE.WebGLRenderer();
        renderer.setSize(400, 400);
        renderWindowContainer.appendChild(renderer.domElement);
        camera.lookAt(new THREE.Vector3(0,0,0));
        camera.position.set( 0, 0, 1 );

        var controls = new OrbitControls( camera, renderer.domElement );
        var geometry = new THREE.Geometry();
        var vertices = document.triangleDataSet.vertices;    
        var faces = document.triangleDataSet.faces;    
        var data = document.triangleDataSet.pointdata;    

        var i = 0;
        for (i = 0; i < vertices.length; i += 3) { 
            geometry.vertices.push(new THREE.Vector3(vertices[i], vertices[i+1], vertices[i+2]));
        }
        console.log(
            document.triangleDataSet,
            faces
        );
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
    display(HTML(html_code_visual))


def passdata(ver, ele, point):
    colord = [ cm.jet(x) for x in point ]
    #div_name = ranstr(4)
    js_code = """
    document.triangleDataSet = %s; 
    console.log(document.triangleDataSet);
    """ % json.dumps({'vertices': ver, 'faces': ele, 'pointdata': colord})
    print("Passing the data...")
    return Javascript(js_code)


def visualization(ver, ele, pointdata):
    passdata(ver, ele, pointdata)
    print("Data converted and passed...")
    print("Display...")
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