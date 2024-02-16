let form = document.forms["info-form"];
form.addEventListener("submit", getValues);

function getValues(event){
	event.preventDefault();

	let data = {
		"occupation": this.Occupation.value, 
		"age": this.Age.value, 
		"gender": this.Gender.value,
		"computerOpSkill": this.ComputerOpSkill.value,
	}

	let	out = `
		<p>Name: <span>${data.occupation}</span></p>
		<p>Bio: <span>${data.age}</span></p>
		<p>Gender: <span>${data.gender}</span></p>
		<p>Fav food: <span>${data.computerOpSkill}</span></p>
	`;

	document.querySelector(".out code").innerHTML = out;
}