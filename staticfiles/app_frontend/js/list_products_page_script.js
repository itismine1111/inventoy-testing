$(document).ready(function () {
  // console.log("ready!");
  // var URL_GET_ALL_LOCATIONS = "/api/get-all-locations/";
  // var URL_GET_ALL_CATEGORIES = "/api/get-all-categories/";
  // var URL_GET_ALL_SUPPLIERS = "/api/get-all-suppliers/";
  // var URL_POST_CREATE_INVENTORY = "/api/create-inventory/"
  // var URL_ADD_GROUPS_FORM = BASE_URL + "/add-groups-form/";
  // var URL_ADD_LOCATIONS_FORM = BASE_URL + "/add-locations-form/";
  // var URL_ADD_CATEGORIES_FORM = BASE_URL + "/add-categories-form/";
  // var URL_ADD_SUPPLIERS_FORM = BASE_URL + "/add-suppliers-form/";
  var BASE_URL = "127.0.0.1:8000";
  var URL_LOGIN = BASE_URL + "/login/";
  var URL_GET_LOGIN_USER_DETAILS =
    "//" + BASE_URL + "/api/get-login-user-details/";
  var URL_GET_ALL_GROUPS = "//" + BASE_URL + "/api/get-all-groups/";
  var URL_GET_ALL_LOCATIONS = "//" + BASE_URL + "/api/get-all-locations/";
  var URL_UPDATE_INVENTORY = "//" + BASE_URL + "/api/update-inventory/";
  var URL_GET_ALL_INVENTORY_SORTED_BY_LOCATIONS =
    "//" + BASE_URL + "/api/get-products-sorted-by-location/";
  let current_login_user = null;
  let focused_field_value = null;
  let focused_field_target = null;
  let last_used_filter_category = "";
  let last_used_filter_category_value = 0;
  let selected_sort = "asc";

  var token = window.localStorage.getItem("token");
  if (!token) {
    // redirect to login page
    window.location.href = "//" + URL_LOGIN;
  }
  var token_string = "token " + token;

  $(".selectpicker").selectpicker();

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

  // Get Login user Details
  function get_login_user_details() {
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


  function get_inventory_and_fill_table(search_by, search, sort) {
    let URL_GET_PRODUCTS;
    last_used_filter_category = search_by;
    last_used_filter_category_value = search;

    if (search === null || search === 0) {
      URL_GET_PRODUCTS = "//" + BASE_URL + "/api/get-products/?sort=" + sort;
    } else {
      URL_GET_PRODUCTS =
        "/api/get-products/?search_by=" +
        search_by +
        "&search=" +
        search +
        "&sort=" +
        sort;
    }

    // alert(URL_GET_PRODUCTS);

    $.ajax({
      type: "GET",
      url: URL_GET_PRODUCTS,
      beforeSend: function (xhr) {
        xhr.setRequestHeader("Authorization", token_string);
      },
      success: function (json_data) {
        console.log(json_data);
        if (json_data["success"] === true) {
          // console.log(json_data);
          $("#list-table-body").html("");
          for (let i = 0; i < json_data["data"]["count"]; i++) {
            // console.log(json_data["data"]["list"][i]["ItemName"]);
            var table_row = document.createElement("tr");
            table_row.setAttribute(
              "data-id",
              json_data["data"]["list"][i]["id"]
            );

            // th - name
            var th_name = document.createElement("th");
            var th_name_input = document.createElement("input");
            th_name_input.setAttribute("type", "text");
            th_name_input.setAttribute(
              "class",
              "form-control change-listener-class"
            );
            th_name_input.setAttribute("id", "");
            th_name_input.setAttribute(
              "placeholder",
              "Comet or Toilet Cleaner"
            );
            th_name_input.setAttribute("name", "ItemName");
            th_name_input.value = json_data["data"]["list"][i]["ItemName"];
            th_name.appendChild(th_name_input);
            table_row.appendChild(th_name);

            // td - Stock
            var td_stock = document.createElement("td");
            var td_stock_input = document.createElement("input");
            td_stock_input.setAttribute("type", "text");
            td_stock_input.setAttribute("class", "form-control");
            td_stock_input.setAttribute("id", "");
            td_stock_input.setAttribute("placeholder", "Stock");
            td_stock_input.value =
              json_data["data"]["list"][i]["units_on_hand_value"];
            td_stock_input.readOnly = true;
            td_stock.appendChild(td_stock_input);
            table_row.appendChild(td_stock);

            // td - Minimum Level
            var td_min_level = document.createElement("td");
            var td_min_level_input = document.createElement("input");
            td_min_level_input.setAttribute("type", "text");
            td_min_level_input.setAttribute(
              "class",
              "form-control change-listener-class"
            );
            td_min_level_input.setAttribute("id", "");
            td_min_level_input.setAttribute("placeholder", "Min Level");
            td_min_level_input.setAttribute("name", "ReorderLevel");
            td_min_level_input.value =
              json_data["data"]["list"][i]["ReorderLevel"];
            td_min_level_input.readOnly = false;
            td_min_level.appendChild(td_min_level_input);
            table_row.appendChild(td_min_level);

            // td - Units Measure
            var td_unit_measure = document.createElement("td");
            var unit_measure_input = document.createElement("input");
            unit_measure_input.setAttribute("type", "text");
            unit_measure_input.setAttribute("class", "form-control");
            unit_measure_input.setAttribute("id", "");
            unit_measure_input.setAttribute("placeholder", "UM");
            // unit_measure_input.value =
            //   json_data["data"]["list"][i]["UnitsMeasure"];
            // FIXME:
            unit_measure_input.value = json_data["data"]["list"][i]["UnitsMeasure"]["name"];
            unit_measure_input.readOnly = true;
            td_unit_measure.appendChild(unit_measure_input);
            table_row.appendChild(td_unit_measure);

            // td - Description
            var td_description = document.createElement("td");
            var description_textarea = document.createElement("textarea");
            description_textarea.setAttribute("type", "text");
            description_textarea.setAttribute(
              "class",
              "form-control change-listener-class"
            );
            description_textarea.setAttribute("id", "");
            description_textarea.setAttribute("placeholder", "Description");
            description_textarea.setAttribute("name", "ItemDescription");
            description_textarea.value =
              json_data["data"]["list"][i]["ItemDescription"];
            description_textarea.setAttribute("rows", "4");
            description_textarea.setAttribute("cols", "8");
            description_textarea.readOnly = false;
            td_description.appendChild(description_textarea);
            table_row.appendChild(td_description);

            // td - Category
            var td_category = document.createElement("td");
            // var category_input = document.createElement("input");
            // category_input.setAttribute("type", "text");
            // category_input.setAttribute("class", "form-control");
            // category_input.setAttribute("id", "");
            // category_input.setAttribute("placeholder", "Category");
            // category_input.value =
            //   json_data["data"]["list"][i]["Category"]["name"];
            // category_input.readOnly = true;
            // td_category.appendChild(category_input);
            // table_row.appendChild(td_category);

            var category_select = document.createElement("select");
            // category_select.setAttribute("class", "form-control");
            category_select.setAttribute("id", "category");
            category_select.setAttribute("placeholder", "Category");
            category_select.setAttribute("multiple", "multiple");
            category_select.setAttribute("disabled", "true");
            category_select.style.width = "100%";

            for(let j=0; j<json_data["data"]["list"][i]["Category"].length; j++){
              var option = document.createElement("option");
              option.innerHTML = json_data["data"]["list"][i]["Category"][j]["name"];
              option.setAttribute("value", json_data["data"]["list"][i]["Category"][j]["id"]);
              option.selected = true;
              category_select.appendChild(option);
            }
            td_category.appendChild(category_select);
            table_row.appendChild(td_category);

            // td - Availability
            var td_availability = document.createElement("td");
            var availability_input = document.createElement("input");
            availability_input.setAttribute("type", "text");
            availability_input.setAttribute("class", "form-control");
            availability_input.setAttribute("id", "");
            availability_input.setAttribute("placeholder", "Availability");
            const stock_availability_array =
              json_data["data"]["list"][i]["stock_availability_value"].split(
                "|"
              );
            availability_input.value = stock_availability_array[0];
            availability_input.style.color = stock_availability_array[1];
            availability_input.readOnly = true;
            td_availability.appendChild(availability_input);
            table_row.appendChild(td_availability);

            // td - Location
            var td_location = document.createElement("td");
            // var location_input = document.createElement("input");
            // location_input.setAttribute("type", "text");
            // location_input.setAttribute("class", "form-control");
            // location_input.setAttribute("id", "");
            // location_input.setAttribute("placeholder", "Location");
            // location_input.value =
            //   json_data["data"]["list"][i]["Location"]["name"];
            // location_input.readOnly = true;
            // td_location.appendChild(location_input);
            // table_row.appendChild(td_location);
            
            var location_select = document.createElement("select");
            // location_select.setAttribute("class", "form-control");
            location_select.setAttribute("id", "location");
            location_select.setAttribute("placeholder", "Location");
            location_select.setAttribute("multiple", "multiple");
            location_select.setAttribute("disabled", "true");
            location_select.style.width = "100%";

            for(let j=0; j<json_data["data"]["list"][i]["Location"].length; j++){
              var option = document.createElement("option");
              option.innerHTML = json_data["data"]["list"][i]["Location"][j]["name"];
              option.setAttribute("value", json_data["data"]["list"][i]["Location"][j]["id"]);
              option.selected = true;
              location_select.appendChild(option);
            }
            td_location.appendChild(location_select);
            table_row.appendChild(td_location);


            document.querySelector("#list-table-body").appendChild(table_row);
          }
          addEventListenerToFields();
          // addEventListenerToPrintBtn();
        }
      },
      error: function (json_data) {
        console.log("ERROR");
      },
    });
  }

  get_inventory_and_fill_table(
    (search_by = "groups"),
    (search = 0),
    (sort = "asc")
  );

  function addEventListenerToFields() {
    const inputs = document.querySelectorAll(".change-listener-class");

    inputs.forEach((i) => {
      i.addEventListener("focusin", function handleClick(event) {
        // console.log('i focusin', event);
        // event.target.style.background = 'pink';
        focused_field_value = i.value;
        // console.log(focused_field_value);
        // console.log(i.getAttribute("name"));
        i.setAttribute("style", "background-color: rgb(218, 222, 230);");
      });

      i.addEventListener("blur", function handleClick(event) {
        // console.log('i focusout', event);
        // event.target.style.background = 'blue';
        // console.log(event.target.value);
        i.setAttribute("style", 'background-color: "white";');
        if (i.value !== focused_field_value) {
          updateField(
            (name_field = i.getAttribute("name")),
            (value_field = i.value),
            (id = $(i).closest("tr").attr("data-id"))
          );
        }
      });
    });
  }

  // FIXME: Api is giving 500 server error but it is updating. I have roved he toast that shows the error
  function updateField(name_field, value_field, id) {
    // console.log("VALUE CHANGED");
    // console.log("OLD: " + focused_field_value);
    // console.log("New: " + value_field);
    // console.log("ID: " + id);

    const formData = new FormData();
    formData.append(name_field, value_field);

    var object = {};
    formData.forEach(function(value, key){
      if(!value || value===""){
        object[key] = null;
      }
      else{
        object[key] = value;
      }
      
    });

  var json = JSON.stringify(object);

    var url = URL_UPDATE_INVENTORY + id + "/";

    $.ajax({
      type: "POST",
      url: url,
      data: json,
      processData: false,
      contentType: "application/json",
      beforeSend: function (xhr) {
        xhr.setRequestHeader("Authorization", token_string);
      },
      success: function (json_data) {
        // alert(json_data);
        if (json_data["success"] === true) {
          // console.log(json_data["data"]);
          showToast("Field Updated", (type = "success"));
        }
      },
      error: function (json_data) {
        console.log("ERROR UPDATING FIELD");
        // showToast("Field update failed", type="warning");
      },
    });
  }

  // home-btn
  var home_btn = document.querySelector("#home-btn");
  home_btn.addEventListener("click", () => {
    window.location.href = "//" + BASE_URL;
  });

  // Get products in asc order
  var sort_asc = document.querySelector("#sort-btn-asc");
  sort_asc.addEventListener("click", () => {
    // alert("clicked");
    selected_sort = "asc";
    get_inventory_and_fill_table(
      last_used_filter_category,
      last_used_filter_category_value,
      "asc"
    );
  });

  // Get products in dec order
  var sort_dec = document.querySelector("#sort-btn-dec");
  sort_dec.addEventListener("click", () => {
    // alert("clicked");
    selected_sort = "asc";
    get_inventory_and_fill_table(
      last_used_filter_category,
      last_used_filter_category_value,
      "dec"
    );
  });

  // function addEventListenerToPrintBtn(){
  // }

  // Print report
  var print_report = document.querySelector("#print-btn");

  print_report.addEventListener("click", () => {
    get_products_by_location_and_print();
  });

  function get_products_by_location_and_print() {
    var url =
      URL_GET_ALL_INVENTORY_SORTED_BY_LOCATIONS +
      "?sort=" +
      selected_sort +
      "/";
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

          var newWin = window.open("", "", "height=650, width=650");
          newWin.document.write("");
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

  var group_search_input = document.querySelector("#group-search-input");
  group_search_input.addEventListener("focusin", () => {
    // alert("focusin");
    var input_field = document.querySelector("#group-search-input")
    fillGroupsSuggestionDiv(input_value = input_field.value);
    document.querySelector("#group-search-results-div").style.display = "block";
    
  });

  $(document).click(function (e) {
    if ($(e.target).is("#group-search-input, #group-search-results-div")) {
      return;
    } else {
      document.getElementById("group-search-results-div").style.display =
        "none";
    }
  });

  group_search_input.addEventListener("keyup", () => {
    document.querySelector("#group-search-results-div").style.display = "block";
    fillGroupsSuggestionDiv((input_value = group_search_input.value));
  });

  function fillGroupsSuggestionDiv(input_value = "") {
    var url = URL_GET_ALL_GROUPS + "?name=" + input_value;

    $.ajax({
      type: "GET",
      url: url,
      beforeSend: function (xhr) {
        xhr.setRequestHeader("Authorization", token_string);
      },
      success: function (json_data) {
        // alert(json_data);
        if (json_data["success"] === true) {
          // alert("Groups");
          console.log(json_data);
          if (json_data["data"]["count"] === 0) {
            document.querySelector("#nothing-found-para").style.display =
              "block";
            document.querySelector(
              "#group-search-suggestion-list"
            ).style.display = "none";
          } else {
            document.querySelector("#nothing-found-para").style.display =
              "none";
            document.querySelector(
              "#group-search-suggestion-list"
            ).style.display = "block";

            var suggestion_box_ul = document.querySelector(
              "#group-search-suggestion-list"
            );
            suggestion_box_ul.innerHTML = "";

            for (let i = 0; i < json_data["data"]["count"]; i++) {
              var item_link = document.createElement("a");
              item_link.setAttribute("class", "list-links-a");
              item_link.setAttribute("href", "javascript:void(0);");
              item_link.dataset.id = json_data["data"]["list"][i]["id"];
              item_link.dataset.name = json_data["data"]["list"][i]["name"];

              var list_item = document.createElement("li");
              list_item.setAttribute("class", "suggestion-list-item");
              list_item.innerHTML = json_data["data"]["list"][i]["name"];

              item_link.appendChild(list_item);
              suggestion_box_ul.appendChild(item_link);
            }

            addingEventListenerToSuggestionBoxLinks();
          }
        }
      },
      error: function (json_data) {
        // alert("ERROR");
        console.log("ERROR URL GET ALL Groups");
      },
    });
  }

  // calling this to fill the suggestion box with all the groups
  fillGroupsSuggestionDiv();

  function addingEventListenerToSuggestionBoxLinks() {
    // get_inventory_and_fill_table(search_by="groups", search="", sort=selected_sort);

    var group_suggestions_a = document.getElementsByClassName("list-links-a");

    for (let i = 0; i < group_suggestions_a.length; i++) {
      group_suggestions_a[i].addEventListener("click", () => {
        get_inventory_and_fill_table(
          (search_by = "groups"),
          (search = group_suggestions_a[i].dataset.id),
          (sort = selected_sort)
        );
        document.querySelector("#group-search-results-div").style.display =
          "none";
        document.querySelector("#group-search-input").value =
          group_suggestions_a[i].dataset.name;
      });
    }

  }
});
