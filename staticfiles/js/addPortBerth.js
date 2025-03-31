document.getElementById("addPort").onclick = function(){
    var section = document.getElementById("portAdd");
    var clone = section.cloneNode(true);
    section.parentNode.insertBefore(clone, section.nextSibling);
};

var placeholderText = "Write all the cargo handled at berth followed by /";
document.getElementById("cargoType").placeholder = placeholderText.replace(/\n/g, ' '); 
