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

function httpPut(theUrl, update_object) {
        var page = new XMLHttpRequest();
        page.open("PUT", theUrl);
        page.send(JSON.stringify(update_object));
};

function httpDelete(theUrl) {
    var page = new XMLHttpRequest();
    page.open("DELETE", theUrl);
    page.send();
};

function mealEntryForm(meal) {

  var form = document.createElement('form');
  form.setAttribute('action', "http://localhost:5000/meals/");
  form.setAttribute('class', 'meal-edit-form');

  var label = document.createElement('label');
  var input = document.createElement('input');

  label.setAttribute('class', 'field');
  label.setAttribute('for', 'name');
  label.innerText = 'name';
  input.setAttribute('type', 'text');
  input.setAttribute('name', 'name');
  try {
    input.value =  meal.name;
  } catch (e) {};

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
      for (key in meal[o]){
        textarea.value += JSON.stringify(meal[o][key]).concat(" ", JSON.stringify(key), "\r\n").replace(/[",]/g,"");
      }
    } catch(e) {};
    form.appendChild(label);
    form.appendChild(textarea);
  });

  return form;

};

function populateMealDBList() {

  // populate database list of meals with functionality

  httpGet(LOCAL_HOST.concat('meals/')).then( function (all_meals) {

    if (all_meals.length < 1){

      console.log("no meals in database!");

    } else {

      var dsp_meals = document.getElementById('db-meal-list');

      all_meals.forEach( function(meal) {

        var meal_addr = LOCAL_HOST.concat('meals/_id/<value>/').replace('<value>', meal._id);
        var entry_parent = document.createElement('div');
        var entry_major = document.createElement("p");
        var entry_minor = document.createElement("p");
        var entry_del_button = document.createElement('button');
        var edit_open = 0;
        var meal_entry_form = mealEntryForm(meal);
        var update_button = document.createElement('button');

        update_button.setAttribute('type','button');
        update_button.innerText = "Update";
        update_button.addEventListener('click', function(evt){
            var update_object = {};
            update_object._id = meal._id;
            var obj_elements = entry_parent.childNodes[0].childNodes;
            var key = "";
            var value = "";
            obj_elements.forEach(function(el){
                if (el.nodeName == "LABEL"){
                    key = el.getAttribute("FOR");
                } else if (el.nodeName == "INPUT" | el.nodeName == "SELECT" | el.nodeName == "TEXTAREA"){
                    value = el.value;
                }
              update_object[key] = value;
            });
            httpPut(meal_addr, update_object);
        });

        entry_parent.setAttribute('id', meal._id);
        entry_del_button.innerHTML = 'Delete';
        entry_del_button.addEventListener('click', function(evt) {
          if (confirm("Are you sure you want to permenantly remove this meal?")) {
            httpDelete(meal_addr);
            entry_parent.parentNode.removeChild(entry_parent);
          }
        });

        meal_entry_form.appendChild(update_button);
        entry_parent.appendChild(meal_entry_form);
        entry_parent.appendChild(entry_del_button);
        dsp_meals.appendChild(entry_parent);

      });
    };
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

function RandomMealGenerator(n) {

  return new Promise( function(resolve, reject) {

    httpGet(LOCAL_HOST.concat('meals/random?n=<n>').replace('<n>', n)).then( function (randomResults) {

      var results_div = document.createElement('div');
      results_div.setAttribute('id', "results");

      randomResults[n.concat(' random meal(s)')].forEach( function (element){

         var result_div = document.createElement('div')
         var meal_name = document.createElement('h4');
         meal_name.innerText = element.name;
         result_div.appendChild(meal_name);

         ingredient_div = document.createElement('div')
         kv_pair = element.ingredients;
         for (key in kv_pair){
           var kv_line = document.createElement('p');
           kv_line.innerText = key.concat(", ").concat(kv_pair[key]);
           ingredient_div.appendChild(kv_line);
           result_div.appendChild(ingredient_div);
         };

         var remove_button = document.createElement('button');
         remove_button.setAttribute('type','button');
         remove_button.innerText= 'remove';
         result_div.append(remove_button);
         remove_button.addEventListener('click', function (evt) {
           this.parentNode.remove();
         });

         results_div.appendChild(result_div);
      });

      var add_button = document.createElement('button');
      add_button.setAttribute('type','button');
      add_button.innerText= 'add';
      add_button.addEventListener('click', function (evt) {
        this.remove(add_button);
        RandomMealGenerator("1").then( function(results_div) {
          var results_parent_div = document.getElementById('results_parent');
          results_parent_div.appendChild(results_div);
        });
      });
      results_div.appendChild(add_button);

      resolve(results_div);

    });
  });
}


function PostMealPlanGeneratorForm() {

  var form = document.createElement('form');
  var label = document.createElement('label');
  var input = document.createElement('input');
  var submit = document.createElement('button');
  var generator_div = document.getElementById("generator");

  input.setAttribute('type', 'text');
  input.setAttribute('name', 'n');

  label.setAttribute('class', 'field');
  label.setAttribute('for', 'name');
  label.innerText = 'Number of Meals';
  label.appendChild(input);

  form.appendChild(label);
  form.setAttribute('class', 'mealplan-form');

  submit.setAttribute('type','button');
  submit.innerText= 'Go!';
  submit.addEventListener('click', function (evt) {

    try { // delete parent element if its already been initialised
      document.getElementById('results_parent').innerHTML = "";
    } catch(e){
      console.log(e);
    };

    // puts random meals into divs and appends to DOM
    RandomMealGenerator(input.value).then( function(results_div) {
      var results_parent_div = document.getElementById('results_parent');
      results_parent_div.appendChild(results_div);
    });
  });

  form.appendChild(submit);
  generator_div.append(form);

};




// main
if (FNAME == 'meal_search.html'){

  populateMealDBList();

} else if (FNAME == 'meal_entry_form.html') {

  POSTMealEntryForm();

} else if (FNAME == 'meal_plan.html'){

  PostMealPlanGeneratorForm();


}
