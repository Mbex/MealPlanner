console.log("Js loading");

var LOCAL_HOST = 'http://127.0.0.1:5000/';

function httpGet(theUrl) {
    return new Promise( function(resolve, reject) {
        page = new XMLHttpRequest();
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



// populate database list
httpGet(LOCAL_HOST.concat('meals/')).then( function (all_meals) {

    var dsp_meals = document.getElementById('db-meal-list');

    all_meals.forEach( function(element) {

      var entry = document.createElement('div');
      var entry_major = document.createElement("p");
      var entry_minor = document.createElement("p");
      var entry_del_button = document.createElement('button');
      var form = document.createElement('form');
      var input = document.createElement('input');

      entry.setAttribute('id',element._id);
      entry_major.innerHTML = element.name;
      entry_minor.innerHTML = JSON.stringify(element.ingredients);
      entry_del_button.innerHTML = 'Delete';

      // input.setAttribute('id', element._id);
      // input.style.display = 'hidden';
      // form.appendChild(input);
      form.setAttribute('method', 'delete');
      form.setAttribute('id','form'.concat(element._id))
      form.style.display = 'hidden';
      form.setAttribute('action', LOCAL_HOST.concat('meals/keyword=id/value=').concat(element._id));
      entry.appendChild(form);

      entry_del_button.addEventListener('click', function(evt) {

        var id = this.parentNode.getAttribute('id');
        var element = document.getElementById(id);
        element.parentNode.removeChild(element);
        getElementById(form.concat(id)).submit();


      });

      entry.appendChild(entry_major);
      entry.appendChild(entry_minor);
      entry.appendChild(entry_del_button);
      dsp_meals.appendChild(entry);

    }

//  dsp_meals.innerHTML = meal_list.tostring();
  )
});


// var xhttp = new XMLHttpRequest();
// xhttp.onreadystatechange = function() {
//    if (this.readyState == 4 && this.status == 200) {
//       // Action to be performed when the document is read;
//    }
// };
