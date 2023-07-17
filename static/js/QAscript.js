// JavaScript Document
     //  点击按钮
      var button = document.getElementById("qabutton");
      var modal = document.getElementById("modal")
      button.onclick = function () {
        modal.style.display = "block";
      };
    //   关闭按钮
      document.getElementById("close").onclick = function () {
      	modal.style.display = "none";
      };
    //   点击其他领域(即弹窗背景)
    window.onclick = function(event){
        if(event.target ==modal){
                modal.style.display = "none";
        }
    }
