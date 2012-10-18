var obj;

function ProcessXML(url) {
  // native  object

  if (window.XMLHttpRequest) {
    // obtain new object
    obj = new XMLHttpRequest();
    // set the callback function
    obj.onreadystatechange = processChange;
    // we will do a GET with the url; "true" for asynch
    obj.open("GET", url, true);
    // null for GET with native object
    obj.send(null);
  // IE/Windows ActiveX object
  } else if (window.ActiveXObject) {
    obj = new ActiveXObject("Microsoft.XMLHTTP");
    if (obj) {
      obj.onreadystatechange = processChange;
      obj.open("GET", url, true);
      // don't send null for ActiveX
      obj.send();
    }
  } else {
    alert("Your browser does not support AJAX");
  }
}
 
  function processChange() {
    if(httpRequest.readyState === 4){
      if(httpRequest.status === 200){
        alert(httpRequest.responseText);
      }else{
        alert('There was a problem with the request.');
      }
    }
  }

  Q='';
  ss='http://localhost:8080/save?c=';
  x=document;
  y=window;
  if(x.selection){Q=x.selection.createRange().text}
  else if(y.getSelection){Q=y.getSelection()}
  else if(x.getSelection){Q=x.getSelection()}
  for(i=0,l=Q.rangeCount;i<l;i++){ ss += escape(Q.getRangeAt(i).toString())+'<br/>'}
  ss+= '&u=' + escape(location.href) + '&t=' + escape(document.title)+'' ;

  ProcessXML(ss)
