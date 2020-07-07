from IPython.core.display import display, HTML
from IPython.display import Javascript
from matplotlib import cm
import json

html_code = """
<style> canvas { width: 50%; height: 50% }</style>
<script src="https://raw.github.com/mrdoob/three.js/master/build/three.js"></script> 
<script src="http://www.script-tutorials.com/demos/382/js/OrbitControls.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r79/three.min.js"></script>  

<div class="output_area">
    <div id="mydiv_fx" style="width:50%;height:50%">
    </div>
    <div id="output">
    </div>
</div>
<script>
// initial set up
var renderWindowContainer = document.getElementById("mydiv_fx");
var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
var renderer = new THREE.WebGLRenderer();
renderer.setSize(400, 400);
renderWindowContainer.appendChild(renderer.domElement);
camera.lookAt(new THREE.Vector3(0,0,0));
camera.position.set( 0, 0, 1 );

var controls = new THREE.OrbitControls( camera, renderer.domElement );
var geometry = new THREE.Geometry();
var vertices = document.triangleData.vertices;    
var faces = document.triangleData.elements;    
var data = document.triangleData.pointdata;    

var color1 = new THREE.Color( 0x444444 );
var color2 = new THREE.Color( 0xFF0000 );
var color3 = new THREE.Color( 0x000000 );
var color4 = new THREE.Color( 0xFF0000 );

for (i = 0; i < vertices.length; i += 3) { 
    geometry.vertices.push(new THREE.Vector3(vertices[i], vertices[i+1], vertices[i+2]));
}
for (i = 0; i < faces.length; i += 3) { 
    geometry.faces.push(new THREE.Face3(faces[i], faces[i+1], faces[i+2]));
}
console.log(
    typeof data,
    typeof faces,
    typeof vertices
);
//var test = data[0].length;
//for (i = 0; i < data.length; i++) { 
    //var colors[i] = new THREE.Color(data[i][0], data[i][1], data[i][2]);
    //var colorn = new THREE.Color( 0.0, 0.0, 0.5 );
//}
var colorn = new THREE.Color( 0.0, 0.0, 0.5 );
var color1 = new THREE.Color( 0.5, 0.0, 0.0 );
var color2 = new THREE.Color( 0.5, 0.0, 0.0 );
var color3 = new THREE.Color( 0.49, 1.0, 0.47 );

geometry.faces[0].vertexColors.push( colorn, color1, color2 );
geometry.faces[1].vertexColors.push( colorn, color2, color3 );

geometry.computeFaceNormals();

var parameters = {
    vertexColors: THREE.VertexColors,
    side: THREE.DoubleSide};

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

def visualization(vertices, faces, pointdata):
    colors = [ cm.jet(x) for x in pointdata ]
    json_data_sum = json.dumps({'vertices': vertices, 'elements': faces, 'colors': colors})
    Javascript(f"document.triangleData = {json_data_sum}")
    display(HTML(html_code))

if __name__ == "__main__":
    vertices = [0, 0, 0,
                1, 0, 0,
                1, 1, 0,
                0, 1, 0]
    faces = [0, 1, 2,
            0, 2, 3]
    point_data = [0.0, 1.0, 2.3, .5]
    visualization(vertices, faces, point_data)