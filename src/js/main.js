console.log("Js loading");

var LOCAL_HOST = 'http://127.0.0.1:5000/';
var FNAME = document.URL.substr(document.URL.lastIndexOf('/')+1);

function httpGet(theUrl) {
    return new Promise( function(resolve, reject) {
        var page = new XMLHttpRequest();
        page.addEventListener('load', function(evt){
            resolve(JSON.parse(this.responseText));
        });
        page.addEventListener('error', function(error){
            reject(error);
        });
        page.open("GET", theUrl);
        page.send();
    });
}


function httpDelete(theUrl) {
        page = new XMLHttpRequest();
        page.open("DELETE", theUrl);
        page.send();
}


function populateMealDBList() {

  // populate database list of meals with functionality
  httpGet(LOCAL_HOST.concat('meals/')).then( function (all_meals) {

    var dsp_meals = document.getElementById('db-meal-list');
    all_meals.forEach( function(meal) {

      var del_addr = LOCAL_HOST.concat('meals/_id/<value>').replace('<value>', meal._id);
      var entry_parent = document.createElement('div');
      var entry_major = document.createElement("p");
      var entry_minor = document.createElement("p");
      var entry_del_button = document.createElement('button');
      var edit_open = 0;

      entry_parent.setAttribute('id', meal._id);
      entry_major.innerHTML = meal.name;
      entry_minor.innerHTML = JSON.stringify(meal.ingredients);
      entry_del_button.innerHTML = 'Delete';
      entry_del_button.addEventListener('click', function(evt) {
        if (confirm("Are you sure you want to permenantly remove this meal?")) {
          httpDelete(del_addr);
          entry_parent.parentNode.removeChild(entry_parent);
        }
      });

      // THIS IS THE EDIT
      // entry_parent.addEventListener('click', function(evt) {
      //
      //   if (edit_open) {
      //     var mefo = document.getElementById('mefo');
      //     mefo.parentNode.removeChild(mefo);
      //     edit_open = 0;
      //   } else {
      //     var mefo = document.createElement('object');
      //     mefo.setAttribute('id', 'mefo');
      //     mefo.setAttribute('type', 'text/html');
      //     mefo.setAttribute('data', 'meal_entry_form_only.html');
      //     entry_parent.appendChild(mefo);
      //     edit_open = 1;
      //   }
      //
      // });

      entry_parent.appendChild(entry_major);
      entry_parent.appendChild(entry_minor);
      entry_parent.appendChild(entry_del_button);
      dsp_meals.appendChild(entry_parent);

    });
  });
};








// main
if (FNAME == 'meal_search.html'){
populateMealDBList()
}
