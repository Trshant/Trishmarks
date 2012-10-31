((function(){
Q='';
  ss='http://localhost:8080/save?c=';
  x=document;
  y=window;
  if(x.selection){Q=x.selection.createRange().text}
  else if(y.getSelection){Q=y.getSelection()}
  else if(x.getSelection){Q=x.getSelection()}
  for(i=0,l=Q.rangeCount;i<l;i++){ ss += escape(Q.getRangeAt(i).toString())+escape('<br/>') }
  ss+= '&u=' + escape(location.href) + '&t=' + escape(document.title)+'' ;
alert('Yo!');
// create a new script element
var scr = document.createElement('script');
// set the src attribute to that url
scr.setAttribute('src', ss);
// insert the script in out page
document.getElementsByTagName('head')[0].appendChild(scr);
alert('Yo!2');
//setTimeout(self.focus(),3000);
// this function should parse responses.. you can do anything you need..
// you can make it general so it would parse all the responses the page receives based on a response field

alert('Yo!3');
}
 )())
