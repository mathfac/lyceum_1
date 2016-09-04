function arrayCreator(){
 this.length=arguments.length;
 for (var i=0; i<this.length; i++){
  this[i]=arguments[i];
 }
}

function nextPos(){
 if (cur<maxImg-1) return cur+1; else return 0;
}

function prevPos(){
 if (cur>0) return cur-1; else return maxImg-1;
}

function _show(){
 document.frmPanel.btnPrev.value=sDesc[prevPos()];
 document.frmPanel.btnCur.value=sDesc[cur];
 document.frmPanel.btnNext.value=sDesc[nextPos()];
}

function next(){
 cur=nextPos();
 imgPrev.src=imgCur.src;
 document['imgCur'].src=imgNext.src;
 _show();
 imgNext.src=sImages[nextPos()];
}

function prev(){
 cur=prevPos();
 imgNext.src=imgCur.src;
 document['imgCur'].src=imgPrev.src;
 _show();
 imgPrev.src=sImages[prevPos()];
}
