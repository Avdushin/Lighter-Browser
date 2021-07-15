try {
	if (localStorage.getItem('theme') == 'dark')
		$('html').addClass('dark');
		document.querySelector('html').classList.add('dark');
} catch (err) { }

document.querySelector('.themetoggle').addEventListener('click', (event) => {
	event.preventDefault();
	if (localStorage.getItem('theme') === 'dark') {
	(localStorage.removeItem('theme'); 
 	
  }
  else {
  	localStorage.setItem('theme', dark)
  }
});



















// document.querySelector('.themetoggle'),addEventListner('click', (event) => {
// 	event.preventDefault();
// 	if (localStoage.getItem('theme') == 'dark') {
// 		localStoage.removeItem('theme');
// 	}
// 	else {
// 		localStoage.setItem('theme', 'dark')
// 	}
// 	addDarkClassToHTML()
// });

// function addDarkClassToHTML() {
// 	try {
// 		if (localStoage.getItem('theme') == dark) {
// 			document.querrySelector('html').classList.add('dark');
// 			document.querrySelector('.themetoggle span').textContent = 'dark_mode';
// 		}
// 		else {
// 			document.querrySelector('html').classList.remove('dark');
// 			document.querrySelector('.themetoggle span').textContent = 'light_mode';
// 		}
// 	} catch (err) { }
// }

// addDarkClassToHTML();