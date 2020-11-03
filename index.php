<html>
<head>

        <!-- CSS only -->
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous">

<!-- JS, Popper.js, and jQuery -->
<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js" integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8shuf57BaghqFfPlYxofvL8/KUEfYiJOMMV+rV" crossorigin="anonymous"></script>
    </head>
<!-- Trigger the modal with a button -->


<!--<form action="index.php">
    <label for="fname">URL</label><br>
    <input type="text" id="fname" name="fname" value="John"><br>
    <input type="submit" value="Submit">
  </form>-->

<?php


$thing=$_GET['fname'];
$thing1=$_GET['-1'];

$arr=array();
if($thing1!=NULL){
    $counter=0;
    while($counter<30){
        
        $thing1=$_GET[strval($counter)];
        if($thing1!=NULL){
            array_push($arr,$thing1);
        }
        $counter++;
    }
}

$thing4="aaa";
if($_GET['-2']!=NULL){
    $thing4=$_GET['-2'];
}

function js_str($s)
{
    return '"' . addcslashes($s, "\0..\37\"\\") . '"';
}

function js_array($array)
{
    $temp = array_map('js_str', $array);
    return '[' . implode(',', $temp) . ']';
}
?>

<!-- Modal -->
<div id="myModal" class="modal fade" role="dialog">
  <div class="modal-dialog">

    <!-- Modal content-->
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal">&times;</button>
        <h4 class="modal-title">Modal Header</h4>
      </div>
      <div id="mainT" class="modal-body">
        <p>Images</p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
      </div>
    </div>

  </div>

</div>
<style>
  .column {
  float: left;
  width: 20%;
  padding: 10px;
}

/* Clear floats after the columns */
.row:after {
  content: "";
  display: table;
  clear: both;
}
</style>

<div id="mainThing">

<!-- Load Font Awesome Icon Library -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

<!-- Buttons to choose list or grid view -->

<style>
   .checkbox-grid li {
  display: block;
  float: left;
  width: 20%;
}
.hidden {
    display: none;
}
</style>

<form action="http://cesion.us/fdl/index.php">
<input class="hidden" type="checkbox" id="-1" name="-1" value="value1" />
<input class="hidden" type="checkbox" id="-2" name="-2" value="value2" />
<ul id="append" class="checkbox-grid">
    <li><input type="checkbox" name="text1" value="value1" /></li>
   
    
</ul>
<input type="submit" value="Submit">
</form>



<a href="http://34.121.31.197:5000/loadMore/">Next 30 Images</a>


<script>
    var a =`<?php echo $thing?>`;
 
    if(a!=""){

        a=a.split("snapshot?");

        
        var code="";
        function makeHttpObject() {
            try {return new XMLHttpRequest();}
            catch (error) {}
             try {return new ActiveXObject("Msxml2.XMLHTTP");}
            catch (error) {}
            try {return new ActiveXObject("Microsoft.XMLHTTP");}
            catch (error) {}

            throw new Error("Could not create HTTP request object.");
        }

        var request = makeHttpObject();
        request.open("GET", "http://34.121.31.197:5000/resnet/?url="+a[0]+"snapshot&"+a[1]+"&count=30", true); //get urls from API
        request.send(null);
        request.onreadystatechange = function() {
        if (request.readyState == 4){

            code=String(request.responseText);
            //console.log(code);
             code=code.split("###"); //split the result
             console.log(code);

             nums=[];
            
             for(u=0;u<code.length-1;u++){
              if(code[u]!=null){     
                 o=code[u].split(".gov/");
                 p=o[1];
                 f=p.split("/");
                 if(f[7]=="4"){
                     
                    document.getElementById("-2").checked = true; //if the image returned is of the zoomed out type, check this so on the repeat search, the engine knows which endpoint to access.
                 }
                 a=f[8];
                 b=f[9].split(".")[0];
                 nums.push(a+"***"+b); //GIBS index of the returned image 
                 console.log(nums);
                }

             }
             
             
             var stuff="";
             var counter=0;
             for(aY=0;aY<=29;aY++){
                     //set tiles to the GIBS image urls
                    stuff+="<li><input type='checkbox' name='"+String(counter)+"' value='"+nums[aY]+"'><img height='200px' width='200px' src='"+code[aY]+"'></img></li>";

                    counter+=1;
                
            
                
             }
             var ide="row"+String(aY);
                console.log(ide);//sanity check to see how mnay images retrieved
                document.getElementById("append").innerHTML=stuff; //set the html string to the tiles interface div
                stuff="";//reset stuff
                
            }
            
            
            

        };
        document.getElementById("-1").checked = true; //checking this invisible checkbox indicates to the webpage that the first search pass has been completed 
        
    }
    else{
        var t=<?php echo js_array($arr)?>; //unpakcage the indexes from the previous instance of this page.

        console.log(t); //sanity check
        final=""
        for(p=0;p<t.length;p++){
            if(p==0){
                final+=t[p];
            }
            else{
                final+="|||"+t[p];
            }
        }
        
        req=`<?php echo $thing4?>`;
        if(req!="aaa"){
            if(req=='value2'){
                         
                        document.getElementById("-2").checked = true;
             }
        }
         function makeHttpObject() {
            try {return new XMLHttpRequest();}
            catch (error) {}
             try {return new ActiveXObject("Msxml2.XMLHTTP");}
            catch (error) {}
            try {return new ActiveXObject("Microsoft.XMLHTTP");}
            catch (error) {}

            throw new Error("Could not create HTTP request object.");
        }
        var request = makeHttpObject();
        if(document.getElementById("-2").checked ==true){
            request.open("GET", "http://34.121.31.197:5000/multiBig/?url="+final+"&count=30", true);
        }
        else{
            request.open("GET", "http://34.121.31.197:5000/multi/?url="+final+"&count=30", true);
        }
        request.send(null);
        
        request.onreadystatechange = function() {
        if (request.readyState == 4){

            code=String(request.responseText);
            //console.log(code);
             code=code.split("###");
             console.log(code);
             nums=[];
             for(u=0;u<code.length;u++){
               if(code[u]!=""){ 
                 console.log(code[u]);
                 o=code[u].split(".gov/");
                 
                 p=o[1];
                 f=p.split("/");
                 a=f[8];
                 b=f[9].split(".")[0];
                 nums.push(a+"***"+b);
               }

             }
              var stuff="";
             var counter=0;
             for(aY=0;aY<=29;aY++){
                
                    stuff+="<li><input type='checkbox' name='"+String(counter)+"' value='"+nums[aY]+"'><img height='200px' width='200px' src='"+code[aY]+"'></img></li>";

                    counter+=1;
                
            
                
             }
             var ide="row"+String(aY);
                console.log(ide);
                document.getElementById("append").innerHTML=stuff;
                stuff="";
            }
            
        };
        document.getElementById("-1").checked = true;

    }


</script>
</html>
