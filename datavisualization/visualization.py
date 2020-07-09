from IPython.core.display import display, HTML
from IPython.display import Javascript
from matplotlib import cm
import json


def display_data():
    html_code_visual = """
    <style> canvas { width: 50%; height: 50% }</style>
    <script src="https://raw.github.com/mrdoob/three.js/master/build/three.js"></script> 
    <script src="http://www.script-tutorials.com/demos/382/js/OrbitControls.js"></script>
    <div class="output_area">
        <div id="mydiv_new" style="width:50%;height:50%">
        </div>
        <div id="outputnew">
        </div>
    </div>
    <script>
    // initial set up
    var renderWindowContainer = document.getElementById("mydiv_new");
    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
    var renderer = new THREE.WebGLRenderer();
    renderer.setSize(400, 400);
    renderWindowContainer.appendChild(renderer.domElement);
    camera.lookAt(new THREE.Vector3(0,0,0));
    camera.position.set( 0, 0, 1 );

    var controls = new THREE.OrbitControls( camera, renderer.domElement );
    var geometry = new THREE.Geometry();
    var vertices = document.triangleDataSet.vertices;    
    var faces = document.triangleDataSet.elements;    
    var data = document.triangleDataSet.colors;    

    for (i = 0; i < vertices.length; i += 3) { 
        geometry.vertices.push(new THREE.Vector3(vertices[i], vertices[i+1], vertices[i+2]));
    }

    console.log(
        document.triangleDataSet,
        data
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


def visualization(vertices, faces, pointdata):
    colors = [ cm.jet(x) for x in pointdata ]
    json_data = json.dumps({'vertices': vertices, 'elements': faces, 'colors': colors})
    Javascript(f"document.triangleDataSet = {json_data}")
    Javascript("console.log(document.triangleDataSet);")
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