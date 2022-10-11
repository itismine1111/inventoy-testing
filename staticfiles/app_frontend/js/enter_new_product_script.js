$(document).ready(function () {
  console.log("ready!");
  let current_login_user = null;
  var BASE_URL = "127.0.0.1:8000";
  var URL_LOGIN = BASE_URL + "/login/";
  var URL_GET_LOGIN_USER_DETAILS = "//" + BASE_URL + "/api/get-login-user-details/";
  var URL_GET_ALL_GROUPS = "//" + BASE_URL + "/api/get-all-groups/";
  var URL_GET_ALL_CATEGORIES = "//" + BASE_URL + "/api/get-all-categories/";
  var URL_GET_ALL_LOCATIONS = "//" + BASE_URL + "/api/get-all-locations/";
  var URL_GET_ALL_SUPPLIERS = "//" + BASE_URL + "/api/get-all-suppliers/";
  var URL_GET_ALL_UM = "//" + BASE_URL + "/api/get-all-units-measure/";
  var URL_POST_CREATE_INVENTORY = "//" + BASE_URL + "/api/create-inventory/";
  var URL_GET_ALL_INVENTORY_SORTED_BY_LOCATIONS =
    "//" + BASE_URL + "/api/get-products-sorted-by-location/";
  var URL_LIST_PAGE = BASE_URL + "/list-page/";
  var URL_ADD_GROUPS_FORM = BASE_URL + "/add-groups-form/";
  var URL_ADD_LOCATIONS_FORM = BASE_URL + "/add-locations-form/";
  var URL_ADD_CATEGORIES_FORM = BASE_URL + "/add-categories-form/";
  var URL_ADD_SUPPLIERS_FORM = BASE_URL + "/add-suppliers-form/";
  var URL_ADD_UNITS_MEASURE_FORM = BASE_URL + "/add-units-measure-form/";
  var ERRORS_IN_FORM = false;
  let uploaded_image_string = null;


  var token = window.localStorage.getItem("token");
  if (!token) {
    // redirect to login page
    window.location.href = "//" + URL_LOGIN;
  }
  var token_string = "token " + token;

  function showToast(message, type) {
    // alert("toasting");
    var color = "#23272b";
    if (type === "warning") {
      color = "#c82333";
    } else if (type === "error") {
      color = "#e0a800";
    } else if (type === "success") {
      color = "#218838";
    }

    var x = document.getElementById("snackbar");
    x.innerHTML = message;
    x.className = "show";
    x.style.backgroundColor = color;
    setTimeout(function () {
      x.className = x.className.replace("show", "");
    }, 3000);
  }

  // showToast("Error encountered while submitting form", (type = "warning"));

  // Get Login user Details
  function get_login_user_details(){
    $.ajax({
      type: "GET",
      url: URL_GET_LOGIN_USER_DETAILS,
      beforeSend: function (xhr) {
        xhr.setRequestHeader("Authorization", token_string);
      },
      success: function (json_data) {
        // alert(json_data);
        if (json_data["success"] === true) {
          current_login_user = json_data["data"];
          // alert(current_login_user);
          
        }
      },
      error: function (json_data) {
        // alert("ERROR");
        console.log("ERROR URL GET LOGIN USER DETAILS");
      },
    });
  }
  get_login_user_details();
  


  // Fill the Location Options
  $.ajax({
    type: "GET",
    url: URL_GET_ALL_LOCATIONS,
    beforeSend: function (xhr) {
      xhr.setRequestHeader("Authorization", token_string);
    },
    success: function (json_data) {
      // alert(json_data);
      if (json_data["success"] === true) {
        populateTheRadioButtons(
          (data = json_data),
          (div_id = "#location-radio-btns"),
          (field_name = "Location")
        );
      }
    },
    error: function (json_data) {
      // alert("ERROR");
      console.log("ERROR URL GET ALL LOCATIONS");
    },
  });

  // Fill the Group Options
  $.ajax({
    type: "GET",
    url: "//" + BASE_URL + "/api/get-all-groups/",
    beforeSend: function (xhr) {
      xhr.setRequestHeader("Authorization", token_string);
    },
    success: function (json_data) {
      // alert(json_data);
      if (json_data["success"] === true) {      
        populateTheRadioButtons(
          (data = json_data),
          (div_id = "#group-radio-btns"),
          (field_name = "Group")
        );
      }
    },
    error: function (json_data) {
      // alert("ERROR");
      console.log("ERROR URL GET ALL Groups");
    },
  });

  // Fill the Catgories Options
  $.ajax({
    type: "GET",
    url: URL_GET_ALL_CATEGORIES,
    beforeSend: function (xhr) {
      xhr.setRequestHeader("Authorization", token_string);
    },
    success: function (json_data) {
      // alert(json_data);
      if (json_data["success"] === true) {
        populateTheRadioButtons(
          (data = json_data),
          (div_id = "#category-radio-btns"),
          (field_name = "Category")
        );
      }
    },
    error: function (json_data) {
      // alert("ERROR");
      console.log("ERROR URL GET ALL Categories");
    },
  });

  function populateTheRadioButtons(data, div_id, field_name) {
    console.log(data);
    console.log(div_id);
    console.log(field_name);
    parent_div = document.querySelector(div_id);
    var radio_btn_id;
    for (let i = 0; i < data["data"]["count"]; i++) {
      radio_btn_id = field_name + String(data["data"]["list"][i]["id"]);
      $("<input>")
        .attr({
          type: "checkbox",
          class: "check form-check-input",
          id: radio_btn_id,
          name: field_name,
          value: data["data"]["list"][i]["id"],
          style: "margin-right:5px; margin-left:5px"
          // style: "margin-right:6px; padding-right:3px;"
          
        })
        .appendTo(parent_div);

      $("<label>")
        .attr({
          style: "margin-right:2px;",
        })
        .html(data["data"]["list"][i]["name"])
        .appendTo(parent_div);
    }
  }

  // FILL THE SUPPLIERS OPTIONS LIST
  $.ajax({
    type: "GET",
    url: URL_GET_ALL_SUPPLIERS,
    beforeSend: function (xhr) {
      xhr.setRequestHeader("Authorization", token_string);
    },
    success: function (json_data) {
      // alert(json_data);
      if (json_data["success"] === true) {
        $("#Supplier").html("");
        // $("#Supplier").append($("<option>").val(0).text("Select Suppliers.."));
        for (let i = 0; i < json_data["data"]["count"]; i++) {
          $("#Supplier").append(
            $("<option>")
              .val(json_data["data"]["list"][i]["id"])
              .text(json_data["data"]["list"][i]["name"])
          );
        }
      }
    },
    error: function (json_data) {
      // alert("ERROR");
      console.log("ERROR GET SUPPLIER DATA");
    },
  });


    // Fill the Units Measure Options
    $.ajax({
      type: "GET",
      url: URL_GET_ALL_UM,
      beforeSend: function (xhr) {
        xhr.setRequestHeader("Authorization", token_string);
      },
      success: function (json_data) {
        console.log(json_data);
        if (json_data["success"] === true) {
          $("#UnitsMeasure").html("");
          // $("#UnitsMeasure").append(
          //   $("<option>").val(0).text("Units Measure..")
          // );
          for (let i = 0; i < json_data["data"]["count"]; i++) {
            $("#UnitsMeasure").append(
              $("<option>")
                .val(json_data["data"]["list"][i]["id"])
                .text(json_data["data"]["list"][i]["name"])
                .attr("data-type", "category")
            );
          }
        }
      },
      error: function (json_data) {
        // alert("ERROR");
        console.log("ERROR GETTING UNITS MEASURES");
      },
    });
  

  // set the date
  var today = new Date();
  var dd = today.getDate();
  var mm = today.getMonth()+1; 
  var yyyy = today.getFullYear();
  if(dd<10){
      dd='0'+dd;
  } 
  if(mm<10) {
      mm='0'+mm;
  } 
  today = yyyy+'-'+mm+'-'+dd;
  document.querySelector("#DateEntered").value = today;

  // set the requested by field
  document.querySelector("#RequestedBy").value = window.localStorage.getItem("user_email")


  // Change the name of categories-options, when a new option is selected
  // Call the get products api on the selected option and fill the products
  $("#Supplier").change(function () {
    var value = $(this).val();
    // alert("Supplier olptions changed");
  });
  //     units: parseFloat(units),
  //     product_id: product_id,

  // var formdata = {
  //     unit_measure: unit_measure,
  //     lot_number: lot_number,
  //     date: date,
  //     user: user,
  //   };

  var submit_btn = document.querySelector("#new-entry-submit-btn");
  submit_btn.addEventListener("click", () => {
    // var is_validated = validateFieldsData();
    // Removing any previous error messages
    const errors = document.querySelectorAll(".error-para");
    errors.forEach(error => {
      error.remove();
    });
    
    var is_validated = form_validations();
    if(is_validated){
      // alert("validation successful")
      var form = document.querySelector("#new-product-form");
      const formData = new FormData(form);

      groups = formData.getAll("Group");
      formData.delete("Group");

      locations = formData.getAll("Location");
      formData.delete("Location");

      categories = formData.getAll("Category");
      formData.delete("Category");

      suppliers = formData.getAll("Supplier");
      formData.delete("Supplier");


      // alert("starting")
      // console.log("Start form data")
      // console.log(groups);
      // console.log(locations);
      // console.log(categories);
      // console.log(suppliers);
      // console.log("End form data");


      for (var [key, value] of formData.entries()) {
        console.log(key, value);
      }

      formData.delete("Image");
      formData.append("Image", uploaded_image_string);

      var object = {};
      formData.forEach(function(value, key){
          if(!value || value===""){
            object[key] = null;
          }
          else{
            object[key] = value;
          }
          
      });

      object['Supplier'] = suppliers;
      object['Group'] = groups;
      object['Location'] = locations;
      object['Category'] = categories;


      var json = JSON.stringify(object);

      $.ajax({
        type: "POST",
        url: URL_POST_CREATE_INVENTORY,
        data: json,
        processData: false,
        contentType: "application/json",
        // data: $("#new-product-form").serialize( ),
        beforeSend: function (xhr) {
          xhr.setRequestHeader("Authorization", token_string);
        },
        success: function (json_data) {
          if (json_data["success"] === true) {
            // alert("SUCCESS");
            showToast("Product added", (type = "success"));
            window.location.href = "//" + BASE_URL;
          }
        },
        error: function (json_data) {
          console.log(json_data);
          console.log("ERROR POST CREATE INVENTORY");
        },
      });

      // console.log(formData.entries());
    
    }
    else{
      // alert("Toasting");
      showToast("Error encountered while submitting form", (type = "warning"));
    }
    
  });


  // Show preview of selected image 
  image_input = document.querySelector("#Image");
  image_input.addEventListener("change", (event) => {
    var product_preview_img = document.querySelector("#product-preview-img");
    product_preview_img.src = URL.createObjectURL(event.target.files[0]);
  });


    // home-btn
    var home_btn = document.querySelector("#home-btn");
    home_btn.addEventListener("click", () => {
      window.location.href = "//" + BASE_URL;
    });

    // forms links
    var add_groups_form_a = document.querySelector("#add-groups-form-a");
    add_groups_form_a.addEventListener("click", () => {
      // alert("clicked");
      window.location.href = "//" + URL_ADD_GROUPS_FORM;
    });

    var add_locations_form_a = document.querySelector("#add-locations-form-a");
    add_locations_form_a.addEventListener("click", () => {
      // alert("clicked");
      window.location.href = "//" + URL_ADD_LOCATIONS_FORM;
    });

    var add_categories_form_a = document.querySelector("#add-categories-form-a");
    add_categories_form_a.addEventListener("click", () => {
      // alert("clicked");
      window.location.href = "//" + URL_ADD_CATEGORIES_FORM;
    });

    var add_suppliers_form_a = document.querySelector("#add-suppliers-form-a");
    add_suppliers_form_a.addEventListener("click", () => {
      // alert("clicked");
      window.location.href = "//" + URL_ADD_SUPPLIERS_FORM;
    });


    // forms links
    var add_groups_form_a = document.querySelector("#add-groups-form-a");
    add_groups_form_a.addEventListener("click", () => {
      // alert("clicked");
      window.location.href = "//" + URL_ADD_GROUPS_FORM;
    });

    var add_locations_form_a = document.querySelector("#add-locations-form-a");
    add_locations_form_a.addEventListener("click", () => {
      // alert("clicked");
      window.location.href = "//" + URL_ADD_LOCATIONS_FORM;
    });

    var add_categories_form_a = document.querySelector("#add-categories-form-a");
    add_categories_form_a.addEventListener("click", () => {
      // alert("clicked");
      window.location.href = "//" + URL_ADD_CATEGORIES_FORM;
    });

    var add_suppliers_form_a = document.querySelector("#add-suppliers-form-a");
    add_suppliers_form_a.addEventListener("click", () => {
      // alert("clicked");
      window.location.href = "//" + URL_ADD_SUPPLIERS_FORM;
    });

    var add_units_measure_form_a = document.querySelector("#add-units-measure-form-a");
    add_units_measure_form_a.addEventListener("click", () => {
      // alert("clicked");
      window.location.href = "//" + URL_ADD_UNITS_MEASURE_FORM;
    });

    // go to list page
    var list_page_btn = document.querySelector("#list-page-btn");
    list_page_btn.addEventListener("click", () => {
      // alert("clicked");
      window.location.href = "//" + URL_LIST_PAGE;
    });


    function validateFieldsData(){
      var item_name = document.querySelector("#ItemName").value;
      if(item_name === null || item_name === "" ){
        item_name.style.borderColor='#e52213';
        ERRORS_IN_FORM = true;
        // alert("here")
      }
    }

    // Print report
  var print_report = document.querySelector("#print-btn");

  print_report.addEventListener("click", () => {
    get_products_by_location_and_print();
  });


  function get_products_by_location_and_print() {
    var url =
      URL_GET_ALL_INVENTORY_SORTED_BY_LOCATIONS;
    // alert(url);
    $.ajax({
      type: "GET",
      url: url,
      beforeSend: function (xhr) {
        xhr.setRequestHeader("Authorization", token_string);
      },
      success: function (json_data) {
        var counting = 0;
        // alert(json_data);
        if (json_data["success"] === true) {
          console.log(json_data["data"]);

          var parent_div = document.createElement("div");
          parent_div.setAttribute("class", "table-div");
          parent_div.setAttribute("id", "list-table-div-printable");
          parent_div.style.padding = "30px";
          parent_div.style.margin = "30px";

          var table_elem = document.createElement("table");
          table_elem.setAttribute("class", "table table-striped");

          var thread_elem = document.createElement("thread");

          var thread_tr = document.createElement("tr");

          var thread_tr_th_num = document.createElement("th");
          thread_tr_th_num.setAttribute("scope", "col");
          thread_tr_th_num.style.width = "3%";
          thread_tr_th_num.innerHTML = "#";

          var thread_tr_th_item_name = document.createElement("th");
          thread_tr_th_item_name.setAttribute("scope", "col");
          thread_tr_th_item_name.style.width = "15%";
          thread_tr_th_item_name.innerHTML = "Item Name";

          var thread_tr_th_item_stock = document.createElement("th");
          thread_tr_th_item_stock.setAttribute("scope", "col");
          thread_tr_th_item_stock.style.width = "5%";
          thread_tr_th_item_stock.innerHTML = "Stock";

          var thread_tr_th_item_min_level = document.createElement("th");
          thread_tr_th_item_min_level.setAttribute("scope", "col");
          thread_tr_th_item_min_level.style.width = "5%";
          thread_tr_th_item_min_level.innerHTML = "Min Level";

          var thread_tr_th_item_um = document.createElement("th");
          thread_tr_th_item_um.setAttribute("scope", "col");
          thread_tr_th_item_um.style.width = "5%";
          thread_tr_th_item_um.innerHTML = "UM";

          var thread_tr_th_item_description = document.createElement("th");
          thread_tr_th_item_description.setAttribute("scope", "col");
          thread_tr_th_item_description.style.width = "20%";
          thread_tr_th_item_description.innerHTML = "Description";

          var thread_tr_th_item_category = document.createElement("th");
          thread_tr_th_item_category.setAttribute("scope", "col");
          thread_tr_th_item_category.style.width = "10%";
          thread_tr_th_item_category.innerHTML = "Category";

          var thread_tr_th_item_availability = document.createElement("th");
          thread_tr_th_item_availability.setAttribute("scope", "col");
          thread_tr_th_item_availability.style.width = "10%";
          thread_tr_th_item_availability.innerHTML = "Availability";

          thread_tr.appendChild(thread_tr_th_num);
          thread_tr.appendChild(thread_tr_th_item_name);
          thread_tr.appendChild(thread_tr_th_item_stock);
          thread_tr.appendChild(thread_tr_th_item_min_level);
          thread_tr.appendChild(thread_tr_th_item_um);
          thread_tr.appendChild(thread_tr_th_item_description);
          thread_tr.appendChild(thread_tr_th_item_category);
          thread_tr.appendChild(thread_tr_th_item_availability);

          thread_elem.appendChild(thread_tr);

          table_elem.appendChild(thread_elem);

          var tbody_elem = document.createElement("tbody");
          tbody_elem.setAttribute("id", "list-table-body-printable");
          tbody_elem.innerHTML = "";

          for (let i = 0; i < json_data["data"]["count"]; i++) {
            // console.log(json_data["data"]["list"][i]["ItemName"]);

            var table_row_location_h = document.createElement("tr");

            var table_row_location_h_td_blank = document.createElement("td");
            table_row_location_h_td_blank.innerHTML = "";

            var table_row_location_h_td_heading = document.createElement("td");
            table_row_location_h_td_heading.innerHTML =
              json_data["data"]["list"][i]["location_name"].italics();
              table_row_location_h_td_heading.style.fontWeight = 600;


            table_row_location_h.appendChild(table_row_location_h_td_blank);
            table_row_location_h.appendChild(table_row_location_h_td_heading);

            tbody_elem.appendChild(table_row_location_h);

            for (
              let j = 0;
              j < json_data["data"]["list"][i]["inventory_count"];
              j++
            ) {
              var tr_inventory = document.createElement("tr");

              var th_row_num = document.createElement("th");
              var p_row_num = document.createElement("p");
              counting = counting + 1;
              p_row_num.innerHTML = counting;
              th_row_num.appendChild(p_row_num);
              tr_inventory.appendChild(th_row_num);

              var td_item_name = document.createElement("td");
              var p_item_name = document.createElement("p");
              p_item_name.innerHTML =
                json_data["data"]["list"][i]["inventory_list"][j]["ItemName"];
              td_item_name.appendChild(p_item_name);
              tr_inventory.appendChild(td_item_name);

              var td_stock = document.createElement("td");
              var p_stock = document.createElement("p");
              p_stock.innerHTML =
                json_data["data"]["list"][i]["inventory_list"][j][
                  "units_on_hand_value"
                ];
              td_stock.appendChild(p_stock);
              tr_inventory.appendChild(td_stock);

              var td_min_level = document.createElement("td");
              var p_min_level = document.createElement("p");
              p_min_level.innerHTML =
                json_data["data"]["list"][i]["inventory_list"][j][
                  "ReorderLevel"
                ];
              td_min_level.appendChild(p_min_level);
              tr_inventory.appendChild(td_min_level);

              var td_um = document.createElement("td");
              var p_um = document.createElement("p");
              // p_um.innerHTML =
              //   json_data["data"]["list"][i]["inventory_list"][j][
              //     "UnitsMeasure"
              //   ];
              // FIXME:
              p_um.innerHTML = json_data["data"]["list"][i]["inventory_list"][j]["UnitsMeasure"]["name"];
              td_um.appendChild(p_um);
              tr_inventory.appendChild(td_um);

              var td_description = document.createElement("td");
              var p_description = document.createElement("p");
              p_description.innerHTML =
                json_data["data"]["list"][i]["inventory_list"][j][
                  "ItemDescription"
                ];
              td_description.appendChild(p_description);
              tr_inventory.appendChild(td_description);

              var td_category = document.createElement("td");
              var p_category = document.createElement("p");
              p_category.innerHTML =
                json_data["data"]["list"][i]["inventory_list"][j]["Category"][
                  "name"
                ];
              td_category.appendChild(p_category);
              tr_inventory.appendChild(td_category);

              var td_availability = document.createElement("td");
              var p_availability = document.createElement("p");
              const availability_array =
                json_data["data"]["list"][i]["inventory_list"][j][
                  "stock_availability_value"
                ].split("|");
              p_availability.innerHTML = availability_array[0];
              p_availability.style.color = availability_array[1];
              td_availability.appendChild(p_availability);
              tr_inventory.appendChild(td_availability);

              tbody_elem.appendChild(tr_inventory);
            }
          }
          table_elem.appendChild(tbody_elem);
          var parent_div_heading = document.createElement("h1");
          parent_div_heading.innerHTML = "Inventory";

          parent_div.appendChild(parent_div_heading);
          parent_div.appendChild(table_elem);

          var newWin = window.open('', '', 'height=650, width=650');
          newWin.document.write('');
          newWin.document.write(parent_div.innerHTML);
          newWin.document.close();
          newWin.print();

        }
      },
      error: function (json_data) {
        console.log("ERROR GETTING PRINTABLE REPORT");
        showToast("Not able to fetch the report", (type = "warning"));
      },
    });
  }


  var item_name = document.getElementById("ItemName");
  item_name.addEventListener("blur",()=>{
    console.log("ITEMNAME");
    var item_known_as = document.getElementById("ItemKnownAs");
    console.log(item_known_as.value);
    if(!item_known_as.value || item_known_as.value===""){
      item_known_as.value = item_name.value; 
    }
  })


  var image_input = document.getElementById("Image");
  image_input.addEventListener("change", ()=>{

    // alert("On changed");
    var file = document.querySelector(
        'input[type=file]')['files'][0];
  
    var reader = new FileReader();
    console.log("next");
      
    reader.onload = function () {
        uploaded_image_string = reader.result.replace("data:", "")
            .replace(/^.+,/, "");
  
        imageBase64Stringsep = uploaded_image_string;
      
        // alert(imageBase64Stringsep);
        // console.log(uploaded_image_string);
    }
    reader.readAsDataURL(file);

  });

//   function imageUploaded() {
//     alert("On changed");
//     var file = document.querySelector(
//         'input[type=file]')['files'][0];
  
//     var reader = new FileReader();
//     console.log("next");
      
//     reader.onload = function () {
//         uploaded_image_string = reader.result.replace("data:", "")
//             .replace(/^.+,/, "");
  
//         imageBase64Stringsep = uploaded_image_string;
  
//         // alert(imageBase64Stringsep);
//         console.log(base64String);
//     }
//     reader.readAsDataURL(file);
// }




  function insertAfter(newNode, existingNode) {
    existingNode.parentNode.insertBefore(newNode, existingNode.nextSibling);
  }


  function form_validations(){
    validated = true;
    // alert("starting validations");

    var item_name = document.getElementById("ItemName");
    if (!item_name.value || item_name.value === ""){
      var errro_para = document.createElement("p");
      errro_para.setAttribute("class", "error-para");
      errro_para.style.color = "red";
      errro_para.innerHTML = "This is a required field"
      insertAfter(errro_para, item_name);
      validated = false;
    } 
    

    var location_verified = false;
    var location_values =  document.querySelectorAll("#location-radio-btns input");

    location_values.forEach((item)=>{
      // console.log(item.checked)
      if (item.checked){ 
        location_verified = true
      }
    })

    if(!location_verified){
      var errro_para = document.createElement("p");
      errro_para.setAttribute("class", "error-para");
      errro_para.style.color = "red";
      errro_para.style.marginLeft = "160px";
      errro_para.innerHTML = "This is a required field"
      insertAfter(errro_para, document.getElementById("location-radio-btns"));
      validated = false;
    }

    // var category_value = $("input[type='radio'][name='Category']:checked").val();
    var category_verified = false;
    var category_values =  document.querySelectorAll("#category-radio-btns input");

    category_values.forEach((item)=>{
      // console.log(item.checked)
      if (item.checked){ 
        category_verified = true
      }
    })
    if(!category_verified){
      var errro_para = document.createElement("p");
      errro_para.setAttribute("class", "error-para");
      errro_para.style.color = "red";
      errro_para.style.marginLeft = "160px";
      errro_para.innerHTML = "This is a required field"
      insertAfter(errro_para, document.getElementById("category-radio-btns"));
      validated = false;
    }

    // var group_value = $("input[type='radio'][name='Category']:checked").val();
    var group_verified = false;
    var group_values =  document.querySelectorAll("#group-radio-btns input");

    group_values.forEach((item)=>{
      // console.log(item.checked)
      if (item.checked){ 
        group_verified = true
      }
    })
    if(!group_verified){
      var errro_para = document.createElement("p");
      errro_para.setAttribute("class", "error-para");
      errro_para.style.color = "red";
      errro_para.style.marginLeft = "160px";
      errro_para.innerHTML = "This is a required field"
      insertAfter(errro_para, document.getElementById("group-radio-btns"));
      validated = false;
    }

    var item_status_value = $("input[type='radio'][name='ItemStatus']:checked").val();
    if(!item_status_value){
      var errro_para = document.createElement("p");
      errro_para.setAttribute("class", "error-para");
      errro_para.style.color = "red";
      errro_para.style.marginLeft = "160px";
      errro_para.innerHTML = "This is a required field"
      insertAfter(errro_para, document.getElementById("item-status-radio-btns"));
      validated = false;
    }

    // var supplier_value = document.getElementById("Supplier").value;
    var supplier_verified = false;
    var supplier_values =  document.querySelectorAll("#Supplier option");

    supplier_values.forEach((item)=>{
      // console.log(item.checked)
      if (item.selected){ 
        supplier_verified = true
      }
    })
    if(!supplier_verified){
      var errro_para = document.createElement("p");
      errro_para.setAttribute("class", "error-para");
      errro_para.style.color = "red";
      // errro_para.style.marginLeft = "160px";
      errro_para.innerHTML = "This is a required field"
      insertAfter(errro_para, document.getElementById("Supplier"));
      validated = false;
    } 

    
    var unit_measures_value = document.getElementById("UnitsMeasure").value;
    if(!unit_measures_value || unit_measures_value === "0"){
      var errro_para = document.createElement("p");
      errro_para.setAttribute("class", "error-para");
      errro_para.style.color = "red";
      // errro_para.style.marginLeft = "160px";
      errro_para.innerHTML = "This is a required field"
      insertAfter(errro_para, document.getElementById("UnitsMeasure"));
      validated = false;
    } 


    return (validated);
  }


});
