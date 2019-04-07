/*
	The JS script to enable drag and drop reordering.

	Usage:
		1. The items to be reordered should be in the form of <li>
		2. The items to be reordered should be placed in a <ul> with ID='container'
		3. Drag and Drop to reorder the items
		4. Click the button with ID='btn' to redirect to the view that handles saving order
		5. The button will triger a link <a> which specifies the URL to be redirected to.

	Reference:
		The code is based on the blog of Laincarl. Appreciate the content shared.
		https://www.jianshu.com/p/a923add40767

	CreatedBy:
		ForMyTutors, 2019 Mar 26
*/


$(document).ready(function(){
	var node = document.querySelector("#container");
	var btn=document.querySelector("#btn");
	var draging = null;
	
	//set the event handler of the container <ul>
	node.ondragstart = function(event) {
		// console.log("start");
		//compatable wiht FireFox requirements, call setData() to enable dragging.
		event.dataTransfer.setData("te", event.target.innerText); 
		//event.dataTransfer.setData("self", event.target);
		draging = event.target;
		// console.log(event);
	}

	//when drag over another element, change the order
	node.ondragover = function(event) {
		//console.log("onDrop over");
		event.preventDefault();
		var target = event.target;
			//make sure the element to be switched is other <li> but not the container nor the element itself
		if (target.nodeName === "LI"&&target !== draging) {
				if (_index(draging) < _index(target)) {
					target.parentNode.insertBefore(draging,target.nextSibling);
				} else {
					target.parentNode.insertBefore(draging, target);
				}
		}
	}

	//get the index of the element being dragged inside the parent element <ul>
	function _index(el) {
		var index = 0;

		if (!el || !el.parentNode) {
			return -1;
		}

		while (el && (el = el.previousElementSibling)) {
			//console.log(el);
			index++;
		}

		return index;
	}

	//the onclick event handler for button, will send the new order as a parameter to the View that handle saving order of elements,
	// check the corresponding <template>.html and <url>.py for more detail information
	btn.onclick=function(){
		var neworder="";
		for (let child of node.children){
			neworder+=String(child.id)+"-";
		}
		neworder=neworder.slice(0,-1);
		var link=document.querySelector("#save");
		newhref=link.href.replace('neworder',neworder);

		$("#save").attr("href",newhref);
		link.click();
	}

})