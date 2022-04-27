paste = function(){

	var paste_domain  = new RegExp("es-piveplus.citroen.com");

	if (paste_domain.test(document.domain) == true){
		
		var client_name = getUrlParameter('client_name');
		var client_surname = getUrlParameter('client_surname');
		var client_phone = getUrlParameter('client_phone');
		var client_email = getUrlParameter('client_email');
		var client_province = getUrlParameter('client_province');
		var client_location = getUrlParameter('client_location');
		var client_postal_code = getUrlParameter('client-postalcode');
		var client_seller = getUrlParameter('client_seller');

		client_seller_value = findSeller(client_seller);

		document.getElementById('cli_Prenom').value = client_name;
		document.getElementById('cli_NomCli').value = client_surname;
		document.getElementById('cli_Mail').value = client_email;
		document.getElementById('cli_TelPriv').value = client_phone;
		document.getElementById('cli_libville').value = client_location;
		document.getElementById('cli_CodVendeur').value = client_seller_value;
		document.getElementById('cli_TitreCivilite').value = 1;
	}
}

getUrlParameter = function(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    var results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
};

findSeller = function(client_seller){
	var seller_combo = document.getElementById("cli_CodVendeur");
	var i = 1;
	for (; i < seller_combo.length; i++) {
  		console.log(seller_combo[i].text);
  		console.log(seller_combo[i].value);
  		if (similarity(client_seller, seller_combo[i].text) >= 0.80){
  			return seller_combo[i].value
		}

	}
}

similarity = function(s1, s2) {

	var longer = s1;
	var shorter = s2;

	if (s1.length < s2.length) {
		longer = s2;
		shorter = s1;
	}

	var longerLength = longer.length;

	if (longerLength == 0) {
		return 1.0;
	}

	return (longerLength - editDistance(longer, shorter)) / parseFloat(longerLength);
}

editDistance = function(s1, s2) {

	s1 = s1.toLowerCase();
	s2 = s2.toLowerCase();

	var costs = new Array();
	for (var i = 0; i <= s1.length; i++) {
		var lastValue = i;
		for (var j = 0; j <= s2.length; j++) {
			if (i == 0)
				costs[j] = j;
			else {
				if (j > 0) {
					var newValue = costs[j - 1];
					if (s1.charAt(i - 1) != s2.charAt(j - 1))
						newValue = Math.min(Math.min(newValue, lastValue),
					costs[j]) + 1;
					costs[j - 1] = lastValue;
					lastValue = newValue;
				}
			}
		}
		if (i > 0)
			costs[s2.length] = lastValue;
	}
	return costs[s2.length];
}

paste();