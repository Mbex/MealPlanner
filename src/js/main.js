var LOCAL_HOST = 'http://localhost:5000/';
var FNAME = document.URL.substr(document.URL.lastIndexOf('/')+1);

function GetHeaders(theUrl){
  var req = new XMLHttpRequest();
  req.open('GET', theUrl, false);
  req.send(null);
  var headers = req.getAllResponseHeaders().toLowerCase();
  alert(headers);
}

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
};

function httpPut(theUrl) {
    return new Promise( function(resolve, reject) {
        var page = new XMLHttpRequest();
        page.addEventListener('load', function(evt){
            resolve(JSON.parse(this.responseText));
        });
        page.addEventListener('error', function(error){
            reject(error);
        });
        page.open("PUT", theUrl);
        page.send();
    });
};

function httpDelete(theUrl) {
    var page = new XMLHttpRequest();
    page.open("DELETE", theUrl);
    // if (page.readyState == 4 && page.status == 200){
    page.send();
    // }
};


function mealEntryForm(meal) {

  var form = document.createElement('form');
  form.setAttribute('action', "http://localhost:5000/api/meals/");
  form.setAttribute('class', 'meal-edit-form');

  var label = document.createElement('label');
  var input = document.createElement('input');

  label.setAttribute('class', 'field');
  label.setAttribute('for', 'name');
  label.innerText = 'name';

  input.setAttribute('type', 'text');
  input.setAttribute('name', 'name');
  try {
    input.setAttribute('placeholder', meal.name);
  } catch(e){};

  form.appendChild(label);
  form.appendChild(input);

  var label = document.createElement('label');
  label.setAttribute('for', 'meal type');
  label.innerHTML = 'Meal Type';
  form.appendChild(label);

  var select = document.createElement('select');
  select.setAttribute('name', 'meal type');
  select.setAttribute('value', 'Meal');

  var types = ['dinner','breakfast','lunch','snack'];
  types.forEach( function(typ) {
    var type = document.createElement('option');
    type.setAttribute('value', typ);
    type.innerHTML = typ;
    try{
      if (typ == meal.meal_type) {
        type.setAttribute('selected', 'selected');
      };
    } catch (e){};
    select.appendChild(type);
    form.appendChild(select);
  });

  options = ['ingredients','method'];
  options.forEach( function(o) {
    var option = document.createElement('option');
    var label = document.createElement('label');

    label.setAttribute('for', o);
    label.innerHTML = o;

    var textarea = document.createElement('textarea');
    textarea.setAttribute('name', o);
    textarea.setAttribute('rows', 10);
    textarea.setAttribute('cols', 30);
    try{
      textarea.value = JSON.stringify(meal[o]);
    }catch(e) {};
    label.appendChild(textarea);
    form.appendChild(label);
  });

  return form;

};


function populateMealDBList() {

  // populate database list of meals with functionality

  httpGet(LOCAL_HOST.concat('api/meals/')).then( function (all_meals) {

    if (all_meals.length < 1){

      console.log("no meals in database!");

    } else {

      var dsp_meals = document.getElementById('db-meal-list');

      all_meals.forEach( function(meal) {

        var meal_addr = LOCAL_HOST.concat('api/meals/_id/<value>').replace('<value>', meal._id);
        var entry_parent = document.createElement('div');
        var entry_major = document.createElement("p");
        var entry_minor = document.createElement("p");
        var entry_del_button = document.createElement('button');
        var edit_open = 0;
        var meal_entry_form = mealEntryForm(meal);
        var submit = document.createElement('input');

        submit.setAttribute('type','Submit');
        submit.setAttribute('value','Submit');
        submit.addEventListener('click', function(evt){
          console.log("post");
          // httpPut(meal_addr, update);
        });

        entry_parent.setAttribute('id', meal._id);
        entry_del_button.innerHTML = 'Delete';
        entry_del_button.addEventListener('click', function(evt) {
          if (confirm("Are you sure you want to permenantly remove this meal?")) {
            httpDelete(meal_addr);
            entry_parent.parentNode.removeChild(entry_parent);
          }
        });

        meal_entry_form.appendChild(submit);
        entry_parent.appendChild(meal_entry_form);
        entry_parent.appendChild(entry_del_button);
        dsp_meals.appendChild(entry_parent);

      });
    }
  });
};


function POSTMealEntryForm() {

  var meal_entry_form = mealEntryForm();
  var title = document.getElementById('entries');
  var submit = document.createElement('input');
  submit.setAttribute('type','submit');
  submit.setAttribute('value','Submit');
  meal_entry_form.setAttribute('method', 'POST');
  meal_entry_form.appendChild(submit);
  title.appendChild(meal_entry_form);

};




// main
if (FNAME == 'meal_search.html'){

  populateMealDBList();

} else if (FNAME == 'meal_entry_form.html') {

  POSTMealEntryForm();

}
