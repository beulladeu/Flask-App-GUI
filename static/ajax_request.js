

function updateData(){	
	fetch("/api/getData")
		.then((data) => {
			return data.json();
		})
		.then((data) => {
		    str = '';
			var opened_key = document.getElementsByClassName("opened")[0];
			var closed_key = document.getElementsByClassName("closed")[0];
		    if(data.data.message == "True"){
		        str = 'OPENED';
				document.getElementById("st").innerHTML = str;
				opened_key.style.display = "block";
				closed_key.style.display = "none";
		    } else{
		        str = 'CLOSED';
				document.getElementById("st").innerHTML = str;
				opened_key.style.display = "none";
				closed_key.style.display = "block";
		    }
			
			console.log(data['data']['message']);
			setTimeout(updateData, 10000);
		})
		.catch((err) => {
			console.log('error');
			setTimeout(updateData, 5000);
		});
}

updateData();
