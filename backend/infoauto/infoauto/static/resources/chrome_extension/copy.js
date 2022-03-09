
CITROEN_PIVE_URL = "https://es-piveplus.citroen.com/piveplus/clients/createClient.do?paramAction=crearCliente&";
ALLOWED_DOMAIN = ["infoauto-backend", "cochesnet", "smartmotorlead"];

copy = function(){

	if (matchInArray(document.domain, ALLOWED_DOMAIN)) {
		var citroen_pive_element = document.getElementById('extra-button');
		var content = document.createTextNode("Citroen Pive");
		var btn = document.createElement('button');
		
		btn.id = 'btn-confirm';
		btn.type="button";
		btn.innerHTML="Citroen Pive";

		btn.addEventListener("click", function (event) {
			event.preventDefault();
			var client_name = document.getElementById('client-name').value;
			var client_surname = document.getElementById('client-surname').value;
			var client_email = document.getElementById('client-email').value;
			var client_province = document.getElementById('client-province').value;
			var client_postalcode = document.getElementById('client-postal-code').value;
			var client_seller = document.getElementById('client-seller').textContent;
			var client_phone = document.getElementById("client-phone").getElementsByTagName("input")[0].value;
			var client_province = document.getElementById("client-province").getElementsByTagName("input")[0].value;
			var client_location = document.getElementById("client-location").getElementsByTagName("input")[0].value;

			var data = {
				client_name: client_name,
				client_surname: client_surname,
				client_phone: client_phone,
				client_email: client_email,
				client_province: client_province,
				client_province: client_province,
				client_location: client_location,
				client_postalcode: client_postalcode,
				client_seller: client_seller
			}

			console.log(data);
			console.log(CITROEN_PIVE_URL + serialize(data));
			window.open(CITROEN_PIVE_URL + serialize(data));
			
		});

		citroen_pive_element.innerHTML = "";
		citroen_pive_element.appendChild(btn);
	}
}

function matchInArray(string, expressions) {
    var len = expressions.length, i = 0;
    for (; i < len; i++) {
        if (string.match(expressions[i])) {
            return true;
        }
    }
    return false;
}

serialize = function(obj) {
  var str = [];
  for (var p in obj)
    if (obj.hasOwnProperty(p)) {
      str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
    }
  return str.join("&");
}

setTimeout(copy, 5000);

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    // listen for messages sent from background.js
    if (request.message === 'change_tab_event') {
		setTimeout(copy, 5000);
    }
});
