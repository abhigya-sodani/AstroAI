<html>
<head>

<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous">


<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js" integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8shuf57BaghqFfPlYxofvL8/KUEfYiJOMMV+rV" crossorigin="anonymous"></script>
    </head>


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


<script>
     function subPasses(indexes, zoomLevel){
       
    

        final=""
        for(p=0;p<indexes.length;p++){
            if(p==0){
                final+=indexes[p];
            }
            else{
                final+="|||"+indexes[p];
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
        if(zoomLevel=='True'){
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
                
                    stuff+="<li><input type='checkbox' id='"+String(counter)+"' value='"+nums[aY]+"'><img height='200px' width='200px' src='"+code[aY]+"'></img></li>";

                    counter+=1;
                
            
                
             }
             var ide="row"+String(aY);
             console.log(ide);
             document.getElementById("append").innerHTML=stuff;
             stuff="";
            }
            
        };
        

    }
    
 
    function makeSearch(){
        
        
        indexes=[];
         
        for(y=0;y<=29;y++){
            if(document.getElementById(y).checked==true){
                indexes.push(document.getElementById(y).value);
            }
        }
        
        subPasses(indexes,localStorage.getItem("zoomOut"));
        
    }
    
</script>



<ul id="append" class="checkbox-grid">
    <li><input type="checkbox" name="text1" value="value1" /></li>
   
    
</ul>
<input onclick="makeSearch()" type="submit" value="Submit">




<a href="http://34.121.31.197:5000/loadMore/">Next 30 Images</a>


<script>
        
           
        a=`<?php echo $_GET['fname']?>`;
        a=a.split("snapshot?");
        console.log(a);
        //http://34.121.31.197:5000/resnet/?url="+a[0]+"snapshot&"+a[1], {mode: 'cors'}
        //var src = fetch("http://34.121.31.197:5000/resnet/?url="+a[0]+"snapshot&"+a[1], {mode: 'cors'});
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
        request.open("GET", "http://34.121.31.197:5000/resnet/?url="+a[0]+"snapshot&"+a[1]+"&count=30", true);
        request.send(null);
        request.onreadystatechange = function() {
        if (request.readyState == 4){

            code=String(request.responseText);
            //console.log(code);
             code=code.split("###");
             console.log(code);

             nums=[];
            
             for(u=0;u<code.length-1;u++){
              if(code[u]!=null){     
                 o=code[u].split(".gov/");
                 p=o[1];
                 f=p.split("/");
                 if(f[7]=="4"){
                     
                    localStorage.setItem('zoomOut', 'True');
                 }
                 else{
                    localStorage.setItem('zoomOut', 'False'); 
                 }
                 a=f[8];
                 b=f[9].split(".")[0];
                 nums.push(a+"***"+b);
                 console.log(nums);
                }

             }
             
             
             var stuff="";
             var counter=0;
             console.log("ksksksks");
             for(aY=0;aY<=29;aY++){
                
                    stuff+="<li><input type='checkbox' id='"+String(counter)+"' value='"+nums[aY]+"'><img height='200px' width='200px' src='"+code[aY]+"'></img></li>";

                    counter+=1;
                
            
                
             }
             var ide="row"+String(aY);
                console.log(ide);
                document.getElementById("append").innerHTML=stuff;
                stuff="";
                
            }
            
            
            

        };
       
        
     
   
    
    
   


</script>
</html>
