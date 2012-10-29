
  if (window.XMLHttpRequest) {
    var obj = new XMLHttpRequest();
  } else if (window.ActiveXObject) {
    var obj = new ActiveXObject("Microsoft.XMLHTTP");
  }

function ProcessXML(url) {
  if (obj) {
      obj.onreadystatechange = processChange;
      obj.open("GET", url, true);
      obj.send();
    } else {
    alert("Your browser does not support AJAX");
  }
}

function processChange() {
  if(obj.readyState === 4){
      if(obj.status === 200){
        alert(obj.responseText);
      }else{
        alert('There was a problem with the request.'+obj.status+' '+obj.readyState);
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

