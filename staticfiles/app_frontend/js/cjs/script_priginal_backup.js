$(document).ready(function () {
    let login_user_details;
    let current_selected_product = null;
    let st_input_active = false;
    let st_in_selected = false;
    let st_out_selected = false;
    let last_used_filter_category = "";
    let last_used_filter_category_value = 0;
    // const BASE_URL = $("#Url").attr("data-url");
    var BASE_URL = "127.0.0.1:8000";
    // var URL_GET_ALL_CATEGORIES = BASE_URL + "api/get-all-categories/";
    // var URL_GET_ALL_CATEGORIES = "/api/get-all-categories/";
    var GET_PRODUCT_URL = "/api";
    var URL_LOGIN = BASE_URL + "/login/";
    var URL_NEW_PRODUCT_ENTRY_FORM = BASE_URL + "/new-product/";
    var URL_LIST_PAGE = BASE_URL + "/list-page/";
    var URL_ADD_GROUPS_FORM = BASE_URL + "/add-groups-form/";
    var URL_ADD_LOCATIONS_FORM = BASE_URL + "/add-locations-form/";
    var URL_ADD_CATEGORIES_FORM = BASE_URL + "/add-categories-form/";
    var URL_ADD_SUPPLIERS_FORM = BASE_URL + "/add-suppliers-form/";
    var URL_ADD_UNITS_MEASURE_FORM = BASE_URL + "/add-units-measure-form/";
    var URL_GET_ALL_GROUPS = "//" + BASE_URL + "/api/get-all-groups/";
    var URL_GET_ALL_CATEGORIES = "//" + BASE_URL + "/api/get-all-categories/";
    var URL_GET_ALL_LOCATIONS = "//" + BASE_URL + "/api/get-all-locations/";
    var URL_GET_ALL_SUPPLIERS = "//" + BASE_URL + "/api/get-all-suppliers/";
    var URL_GET_ALL_UM = "//" + BASE_URL + "/api/get-all-units-measure/";
    var URL_BASE_DELETE_INVENTORY = "//" + BASE_URL + "/api/delete-inventory/";
    var URL_GET_ALL_INVENTORY_SORTED_BY_LOCATIONS =
      "//" + BASE_URL + "/api/get-products-sorted-by-location/";
    var token = window.localStorage.getItem("token");
    let selected_sort = "asc";
    let focused_field_value = null;
    // console.log(token)
  
    if (!token) {
      // redirect to login page
      // console.log("token" + token);
      window.location.href = "//" + URL_LOGIN;
    }
  
    var token_string = "token " + token;
  
    //Humburgermenu
    let menu = document.querySelector(".menu");
    let openBtn = document.querySelector(".open-btn");
    let closeBtn = document.querySelector(".close-btn");
  
    let logout_btn = document.querySelector("#logout-btn");
    logout_btn.addEventListener("click", () => {
      window.localStorage.removeItem("token");
      window.location.href = "//" + URL_LOGIN;
    });
  
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
    // showToast("No Product is selected", type="warning");
  
    closeBtn.addEventListener("click", () => {
      menu.classList.remove("active-menu");
    });
    openBtn.addEventListener("click", () => {
      menu.classList.add("active-menu");
    });
  
    // FILL THE CATEGORIES OPTIONS LIST
    $.ajax({
      type: "GET",
      url: URL_GET_ALL_CATEGORIES,
      beforeSend: function (xhr) {
        xhr.setRequestHeader("Authorization", token_string);
      },
      success: function (json_data) {
        // alert(json_data);
        if (json_data["success"] === true) {
          $("#categories-options").html("");
          $("#categories-options").append(
            $("<option>").val(0).text("Select Category..")
          );
          for (let i = 0; i < json_data["data"]["count"]; i++) {
            $("#categories-options").append(
              $("<option>")
                .val(json_data["data"]["list"][i]["id"])
                .text(json_data["data"]["list"][i]["name"])
            );
          }
        }
      },
      error: function (json_data) {
        // alert("ERROR");
        console.log("ERROR");
      },
    });
  
  
    function fillCategoriesLocationsGroupsUMSuppliers() {
      // FILL THE CATEGORIES OPTIONS LIST
      $.ajax({
        type: "GET",
        url: URL_GET_ALL_CATEGORIES,
        beforeSend: function (xhr) {
          xhr.setRequestHeader("Authorization", token_string);
        },
        success: function (json_data) {
          // alert(json_data);
          if (json_data["success"] === true) {
            $("#product-category-options").html("");
            $("#product-category-options").append(
              $("<option>").val(0).text("Select Category..")
            );
            for (let i = 0; i < json_data["data"]["count"]; i++) {
              $("#product-category-options").append(
                $("<option>")
                  .val(json_data["data"]["list"][i]["id"])
                  .text(json_data["data"]["list"][i]["name"])
              );
            }
          }
        },
        error: function (json_data) {
          // alert("ERROR");
          console.log("ERROR PRODUCT CATEGORIES OPTIONS");
        },
      });
  
      // FILL THE LOCATIONS OPTIONS LIST
      $.ajax({
        type: "GET",
        url: URL_GET_ALL_LOCATIONS,
        beforeSend: function (xhr) {
          xhr.setRequestHeader("Authorization", token_string);
        },
        success: function (json_data) {
          // alert(json_data);
          if (json_data["success"] === true) {
            $("#product-location-options").html("");
            $("#product-location-options").append(
              $("<option>").val(0).text("Select Location..")
            );
            for (let i = 0; i < json_data["data"]["count"]; i++) {
              $("#product-location-options").append(
                $("<option>")
                  .val(json_data["data"]["list"][i]["id"])
                  .text(json_data["data"]["list"][i]["name"])
              );
            }
          }
        },
        error: function (json_data) {
          // alert("ERROR");
          console.log("ERROR PRODUCT LOCATIONS OPTIONS");
        },
      });
  
      // FILL THE GROUPS OPTIONS LIST
      $.ajax({
        type: "GET",
        url: URL_GET_ALL_GROUPS,
        beforeSend: function (xhr) {
          xhr.setRequestHeader("Authorization", token_string);
        },
        success: function (json_data) {
          // alert(json_data);
          if (json_data["success"] === true) {
            $("#product-group-options").html("");
            $("#product-group-options").append(
              $("<option>").val(0).text("Select Group..")
            );
            for (let i = 0; i < json_data["data"]["count"]; i++) {
              $("#product-group-options").append(
                $("<option>")
                  .val(json_data["data"]["list"][i]["id"])
                  .text(json_data["data"]["list"][i]["name"])
              );
            }
          }
        },
        error: function (json_data) {
          // alert("ERROR");
          console.log("ERROR PRODUCT GROUPS OPTIONS");
        },
      });
  
      // FILL THE SUPPLIER OPTIONS LIST
      $.ajax({
        type: "GET",
        url: URL_GET_ALL_SUPPLIERS,
        beforeSend: function (xhr) {
          xhr.setRequestHeader("Authorization", token_string);
        },
        success: function (json_data) {
          // alert(json_data);
          if (json_data["success"] === true) {
            $("#product-supplier-options").html("");
            $("#product-supplier-options").append(
              $("<option>").val(0).text("Select Supplier..")
            );
            for (let i = 0; i < json_data["data"]["count"]; i++) {
              $("#product-supplier-options").append(
                $("<option>")
                  .val(json_data["data"]["list"][i]["id"])
                  .text(json_data["data"]["list"][i]["name"])
              );
            }
          }
        },
        error: function (json_data) {
          // alert("ERROR");
          console.log("ERROR PRODUCT SUPPLIER OPTIONS");
        },
      });
  
      // FILL THE UNITS MEASURE OPTIONS LIST
      $.ajax({
        type: "GET",
        url: URL_GET_ALL_UM,
        beforeSend: function (xhr) {
          xhr.setRequestHeader("Authorization", token_string);
        },
        success: function (json_data) {
          // alert(json_data);
          if (json_data["success"] === true) {
            $("#product-um-options").html("");
            $("#product-um-options").append(
              $("<option>").val(0).text("Select UM..")
            );
            for (let i = 0; i < json_data["data"]["count"]; i++) {
              $("#product-um-options").append(
                $("<option>")
                  .val(json_data["data"]["list"][i]["id"])
                  .text(json_data["data"]["list"][i]["name"])
              );
            }
          }
        },
        error: function (json_data) {
          // alert("ERROR");
          console.log("ERROR PRODUCT SUPPLIER OPTIONS");
        },
      });
    }
  
      fillCategoriesLocationsGroupsUMSuppliers();
  
  
    // Change the name of categories-options, when a new option is selected
    // Call the get products api on the selected option and fill the products
    $("#categories-options").change(function () {
      var value = $(this).val();
      // alert("Categories olptions changed");
      get_products_and_fill_list("categories", value, "asc");
    });
  
    $("#categories-options").trigger("change");
  
    // Function to fill the products list
    function get_products_and_fill_list(search_by, search, sort) {
      let URL_GET_PRODUCTS;
      last_used_filter_category = search_by;
      last_used_filter_category_value = search;
  
      if (search ===null || search === 0) {
        URL_GET_PRODUCTS = "/api/get-products/";
      } else {
        URL_GET_PRODUCTS =
          "/api/get-products/?search_by=" +
          search_by +
          "&search=" +
          search +
          "&sort=" +
          sort;
      }
  
      alert(URL_GET_PRODUCTS);
  
      $.ajax({
        type: "GET",
        url: URL_GET_PRODUCTS,
        beforeSend: function (xhr) {
          xhr.setRequestHeader("Authorization", token_string);
        },
        success: function (json_data) {
          // alert(json_data);
          if (json_data["success"] === true) {
            // console.log(json_data["data"]);
            $(".buttons-container").html("");
            for (let i = 0; i < json_data["data"]["count"]; i++) {
              var product_button = $(document.createElement("button")).prop({
                type: "button",
                innerHTML: json_data["data"]["list"][i]["ItemName"],
                id: json_data["data"]["list"][i]["id"],
                class: "product-button",
              });
              $(product_button).css({ "text-align": "left", padding: "6px" });
              $(".buttons-container").append(product_button);
              $("#total-count").html(json_data["data"]["count"]);
            }
            add_event_listener_to_buttons();
          }
        },
        error: function (json_data) {
          console.log("ERROR");
        },
      });
    }
  
    // Adding event listener in buttons and calling the fill product details on button click
    function add_event_listener_to_buttons() {
      // alert("Button  listener is being added");
      let buttons = document.querySelectorAll(".product-button");
      buttons.forEach((item, index) => {
        let selectedIndex;
        item.addEventListener("click", () => {
          item.classList.add("active-button");
          selectedIndex = index;
          buttons.forEach((innerItem, i) => {
            if (selectedIndex !== i) {
              innerItem.classList.remove("active-button");
            }
          });
          // alert(item.id);
          getProductDetailsAndFillProductFormData(item.id);
          getSdsDetailsAndFillSdsFormData(item.id);
          getAllStockTransactionsAndAppend(item.id);
        });
      });
    }
  
    // filling the product details on the form after the selecting a product from product buttons list
    function getProductDetailsAndFillProductFormData(id) {
      let URL_GET_PRODUCT_DETAILS = "/api/get-product/" + id + "/";
      // alert(URL_GET_PRODUCT_DETAILS);
      // console.log(URL_GET_PRODUCT_DETAILS);
  
      $.ajax({
        type: "GET",
        url: URL_GET_PRODUCT_DETAILS,
        beforeSend: function (xhr) {
          xhr.setRequestHeader("Authorization", token_string);
        },
        success: function (json_data) {
          // alert(json_data);
          console.log(json_data);
          // console.log("Idhar dekh abbe");
          current_selected_product = json_data["data"]["list"];
          // console.log(current_selected_product);
          if (json_data["success"] === true) {
            // console.log("product details");
            // console.log(json_data["data"]);
  
            // fillCategoriesLocationsGroupsUMSuppliers();
            $("#record-id").html(json_data["data"]["list"]["id"]);
            // filling the product form data
            // $("#").val(json_data['data']['list']['']);
            // console.log(json_data["data"]["list"]["DateEntered"]);
            // console.log(json_data["data"]["list"]["ItemName"]);
            if (json_data["data"]["list"]["DateEntered"] !== null) {
              $("#product-date-entered").val(
                json_data["data"]["list"]["DateEntered"].slice(0, 10)
              );
            } else {
              $("#product-date-entered").val(
                json_data["data"]["list"]["DateEntered"].slice(0, 10)
              );
            }
  
            $("#product-name-heading").html(
              json_data["data"]["list"]["ItemName"]
            );
            $("#product-name").val(json_data["data"]["list"]["ItemName"]);
            $("#product-known-as").val(json_data["data"]["list"]["ItemKnownAs"]);
            $("#product-description").val(
              json_data["data"]["list"]["ItemDescription"]
            );
            if (json_data["data"]["list"]["DateExpired"] !== null) {
              $("#product-date-expired").val(
                json_data["data"]["list"]["DateExpired"].slice(0, 10)
              );
            } else {
              $("#product-date-expired").val(
                json_data["data"]["list"]["DateExpired"]
              );
            }
  
            $("#product-model-year").val(json_data["data"]["list"]["ModelYear"]);
  
            $("#product-part-number").val(
              json_data["data"]["list"]["PartNumber"]
            );
  
            $("#product-barcode-label").val(json_data["data"]["list"]["BarCode"]);
            const stock_availability_array =
              json_data["data"]["list"]["stock_availability_value"].split("|");
            $("#product-stock-status").val(stock_availability_array[0]);
            $("#product-stock-status").css("color", stock_availability_array[1]);
  
            // $("#product-status").html("");
            // $("#product-status").append(
            //   "<option>" + json_data["data"]["list"]["ItemStatus"] + "</option>"
            // );
  
            if(json_data["data"]["list"]["ItemStatus"] === null){
              document.querySelector("#product-status-options").value = 0;
            }
            else {
              console.log("STATIS : " + json_data["data"]["list"]["ItemStatus"]);
              document.querySelector("#product-status-options").value = json_data["data"]["list"]["ItemStatus"];
            }
  
            // $("#product-group-options").html("");
            // $("#product-group-options").append(
            //   "<option>" +
            //     json_data["data"]["list"]["Group"]["name"] +
            //     "</option>"
            // );
            document.querySelector("#product-group-options").value = json_data["data"]["list"]["Group"]["id"];
  
            // $("#product-category-options").html("");
            // $("#product-category-options").append(
            //   "<option>" +
            //     json_data["data"]["list"]["Category"]["name"] +
            //     "</option>"
            // );
            document.querySelector("#product-category-options").value = json_data["data"]["list"]["Category"]["id"];
  
  
              // $("#product-location-options").html("");
              // $("#product-location-options").append(
              //   "<option>" +
              //     json_data["data"]["list"]["Location"]["name"] +
              //     "</option>"
              // );
            document.querySelector("#product-location-options").value = json_data["data"]["list"]["Location"]["id"]
  
            // $("#product-supplier-options").html("");
            // $("#product-supplier-options").append(
            //   "<option>" +
            //     json_data["data"]["list"]["Supplier"]["name"] +
            //     "</option>"
            // );
            console.log("supplier : " + json_data["data"]["list"]["Supplier"]["id"]);
            console.log("Category : " + json_data["data"]["list"]["Category"]["id"]);
            console.log("Group : " + json_data["data"]["list"]["Group"]["id"]);
            console.log("Location : " + json_data["data"]["list"]["Location"]["id"]);
            document.querySelector("#product-supplier-options").value = json_data["data"]["list"]["Supplier"]["id"];
  
            $("#product-units-on-hand").val(
              json_data["data"]["list"]["units_on_hand_value"]
            );
            
            if (json_data["data"]["list"]["UnitsMeasure"]["id"] === null){
              document.querySelector("#product-um-options").value = 0;
            }
            else{
              document.querySelector("#product-um-options").value = json_data["data"]["list"]["UnitsMeasure"]["id"];
            }
            
  
            $("#product-reorder-level").val(
              json_data["data"]["list"]["ReorderLevel"]
            );
            $("#product-min-order").val(
              json_data["data"]["list"]["MinimumOrder"]
            );
  
            if (json_data["data"]["list"]["DateLastOrdered"] !== null) {
              $("#product-date-last-ordered").val(
                json_data["data"]["list"]["DateLastOrdered"].slice(0, 10)
              );
            } else {
              $("#product-date-last-ordered").val(
                json_data["data"]["list"]["DateLastOrdered"]
              );
            }
  
            $("#product-unit-price").val(
              json_data["data"]["list"]["StockUnitPrice"]
            );
            if (json_data["data"]["list"]["DateLastUsed"] !== null) {
              $("#product-date-last-used").val(
                json_data["data"]["list"]["DateLastUsed"].slice(0, 10)
              );
            } else {
              $("#product-date-last-used").val(
                json_data["data"]["list"]["DateLastUsed"]
              );
            }
  
            $("#product-taxable").val(json_data["data"]["list"]["Taxable"]);
            if (json_data["data"]["list"]["DateModified"] !== null) {
              $("#product-last-modified").val(
                json_data["data"]["list"]["DateModified"].slice(0, 10)
              );
            } else {
              $("#product-last-modified").val(
                json_data["data"]["list"]["DateModified"]
              );
            }
  
            $("#product-tax").val(json_data["data"]["list"]["tax_amt_value"]);
            $("#product-delivery-charge").val(
              json_data["data"]["list"]["DeliveryCharge"]
            );
            $("#product-stock-ext-value").val(
              json_data["data"]["list"]["stock_ext_value"]
            );
            $("#product-total-value").val(
              json_data["data"]["list"]["tax_amt_value"]
            );
  
            $("#sds-requested-by").val(json_data["data"]["list"]["RequestedBy"]);
  
            if (json_data["data"]["list"]["RequestedByDate"] !== null) {
              $("#sds-requested-by-date").val(
                json_data["data"]["list"]["RequestedByDate"].slice(0, 10)
              );
            } else {
              $("#sds-requested-by-date").val(
                json_data["data"]["list"]["RequestedByDate"]
              );
            }
  
            $("#sds-approved-by").val(
              json_data["data"]["list"]["RequestApprovedBy"]
            );
  
            if (json_data["data"]["list"]["RequestApprovedDate"] !== null) {
              $("#sds-approved-by-date").val(
                json_data["data"]["list"]["RequestApprovedDate"].slice(0, 10)
              );
            } else {
              $("#sds-approved-by-date").val(
                json_data["data"]["list"]["RequestApprovedDate"]
              );
            }
          }
  
          if (json_data["data"]["list"]["SDSOnFile"] === true) {
            document.getElementById("sds-on-file-checkbox").checked = true;
          } else {
            document.getElementById("sds-on-file-checkbox").checked = false;
          }
  
          $("#product-image").attr(
            "src",
            "//" + BASE_URL + json_data["data"]["list"]["Image"]
          );
        },
        error: function (json_data) {
          console.log("ERROR :  Get Product Details");
        },
      });
    }
  
    function getAllStockTransactionsAndAppend(id) {
      // it is for add transactions
      st_input_active = false;
  
      let URL_GET_STOCK_TRANSACTIONS =
        "/api/get-inventory-stock-transaction/" + id + "/";
      // alert(URL_GET_PRODUCT_DETAILS);
      // console.log(URL_GET_PRODUCT_DETAILS);
  
      $.ajax({
        type: "GET",
        url: URL_GET_STOCK_TRANSACTIONS,
        beforeSend: function (xhr) {
          xhr.setRequestHeader("Authorization", token_string);
        },
        success: function (json_data) {
          // alert(json_data);
          if (json_data["success"] === true) {
            console.log("Stock Transactions Data");
            console.log(json_data["data"]);
            var st_table_body = document.querySelector("#st-table-body");
            st_table_body.innerHTML = "";
  
            for (let i = 0; i < json_data["data"]["count"]; i++) {
              var table_row = document.createElement("tr");
              table_row.setAttribute("id", json_data["data"]["list"][i]["id"]);
              table_row.setAttribute("class", "st-table-row");
              table_row.setAttribute(
                "data-productid",
                json_data["data"]["list"][i]["IDRecord"]
              );
              table_row.setAttribute(
                "data-id",
                json_data["data"]["list"][i]["id"]
              );
  
              // td - date
              var td_date = $(document.createElement("td"));
              if (json_data["data"]["list"][i]["DateTransaction"] !== null) {
                $(td_date).html(
                  json_data["data"]["list"][i]["DateTransaction"].slice(0, 10)
                );
              } else {
                $(td_date).html(json_data["data"]["list"][i]["DateTransaction"]);
              }
  
              $(table_row).append(td_date);
              st_table_body.append(table_row);
  
              // td - calander icon in a link
              var td_calander = $(document.createElement("td"));
  
              var td_calender_a = $(document.createElement("a")).prop({
                class: "dropdown-toggle waves-effect waves-light font-20",
              });
              $(td_calender_a).attr("data-toggle", "dropdown");
  
              var td_calender_i = $(document.createElement("i")).prop({
                class: "fa-regular fa-calendar-days",
              });
  
              $(td_calender_a.append(td_calender_i));
              $(td_calander).append(td_calender_a);
              $(table_row).append(td_calander);
  
              // td- Lot Number
              var td_lot_number = $(document.createElement("td"));
              $(td_lot_number).html(json_data["data"]["list"][i]["LotNumber"]);
              $(table_row).append(td_lot_number);
  
              // td- Description
              var td_description = $(document.createElement("td"));
              $(td_description).html(json_data["data"]["list"][i]["Description"]);
              $(table_row).append(td_description);
  
              // td - Units in a link
              var td_units = $(document.createElement("td")).prop({
                class: "text-nowrap",
              });
  
              var td_units_a = $(document.createElement("a"));
              $(td_units_a).attr("data-toggle", "tooltip");
              $(td_units_a).attr("data-original-title", "Edit");
  
              $(td_units).append(td_units_a);
              $(td_units).append(json_data["data"]["list"][i]["Units"]);
              $(table_row).append(td_units);
  
              // td - units_measure in a link
              var td_units_measure = $(document.createElement("td")).prop({
                class: "text-nowrap",
              });
  
              var td_units_measure_a = $(document.createElement("a"));
              $(td_units_measure_a).attr("data-toggle", "tooltip");
              $(td_units_measure_a).attr("data-original-title", "Edit");
  
              $(td_units_measure).append(td_units_measure_a);
              $(td_units_measure).append(
                json_data["data"]["list"][i]["UnitsMeasure"]
              );
              $(table_row).append(td_units_measure);
  
              // td - buttons in a link
              var td_buttons = $(document.createElement("td")).prop({
                class: "text-nowrap",
              });
  
              var td_buttons_a = $(document.createElement("a"));
              $(td_units_a).attr("data-toggle", "tooltip");
              $(td_units_a).attr("data-original-title", "Close");
  
              var td_buttons_div = $(document.createElement("div")).prop({
                class: "btn-group",
              });
  
              var td_button_in = $(document.createElement("button")).prop({
                class: "btn btn-default btn-outline waves-effect",
                type: "button",
              });
              $(td_button_in).html("In");
  
              var td_button_out = $(document.createElement("button")).prop({
                class: "btn btn-default btn-outline waves-effect",
                type: "button",
              });
              $(td_button_out).html("Out");
  
              if (json_data["data"]["list"][i]["Type"] === "In") {
                $(td_button_in).css("background-color", "rgb(247, 171, 52)");
                $(td_button_in).css("color", "white");
              } else {
                $(td_button_out).css("background-color", "rgb(247, 171, 52)");
                $(td_button_out).css("color", "white");
              }
  
              $(td_buttons_div).append(td_button_in);
              $(td_buttons_div).append(td_button_out);
              $(td_buttons_a).append(td_buttons_div);
              $(td_buttons).append(td_buttons_a);
              $(table_row).append(td_buttons);
  
              // td - delete button in a link
              var td_del_btn = $(document.createElement("td")).prop({
                class: "text-nowrap",
              });
  
              var td_del_btn_a = $(document.createElement("a")).prop({
                class:
                  "dropdown-toggle waves-effect waves-light font-20 st-del-button",
                href: "javascript:void(0);",
              });
              $(td_del_btn_a).attr("data-toggle", "dropdown");
  
              var td_del_btn_i = $(document.createElement("i")).prop({
                class: "fa-solid fa-trash-can",
              });
  
              $(td_del_btn_a).append(td_del_btn_i);
              $(td_del_btn).append(td_del_btn_a);
              $(table_row).append(td_del_btn);
            }
  
            add_event_listener_to_delete_buttons_in_st();
          }
        },
        error: function (json_data) {
          console.log("ERROR: Getting Stock Transactions data");
        },
      });
    }
  
    // Adding event listener to delete buttons in stock transaction table
    function add_event_listener_to_delete_buttons_in_st() {
      // alert("Button  listener is being added");
      let buttons = document.querySelectorAll(".st-del-button");
      buttons.forEach((item, index) => {
        item.addEventListener("click", () => {
          var parent_tr = item.closest("tr");
          console.log(parent_tr);
          product_id = $(parent_tr).attr("data-productid");
          stock_transaction_id = $(parent_tr).attr("data-id");
          // deleteStockTransactionAndRefreshTable(stock_transaction_id, product_id);
          swal({
            title: "Are you sure?",
            text: "Delete the entry",
            icon: "warning",
            buttons: true,
            dangerMode: true,
          }).then((willDelete) => {
            if (willDelete) {
              deleteStockTransactionAndRefreshTable(
                stock_transaction_id,
                product_id
              );
              showToast("Entry successfully deleted", (type = "success"));
            } else {
            }
          });
        });
      });
    }
  
    function deleteStockTransactionAndRefreshTable(
      stock_transaction_id,
      product_id
    ) {
      console.log("Product_id : " + product_id);
      console.log("ST_id : " + stock_transaction_id);
  
      let URL_DEL_ST_ENTRY =
        "/api/delete-inventory-stock-transaction/" + stock_transaction_id + "/";
      console.log("URL Del St Entry : " + URL_DEL_ST_ENTRY);
  
      $.ajax({
        type: "POST",
        url: URL_DEL_ST_ENTRY,
        beforeSend: function (xhr) {
          xhr.setRequestHeader("Authorization", token_string);
        },
        success: function (json_data) {
          if (json_data["success"] === true) {
            console.log(json_data["data"]);
            getAllStockTransactionsAndAppend(product_id);
          }
        },
        error: function (json_data) {
          console.log("ERROR DEL ST Entry");
        },
      });
    }
  
    // filling the sds record details for the selected product
    function getSdsDetailsAndFillSdsFormData(product_id) {
      // alert("Reaching here");
      let URL_GET_SDS_DETAILS =
        "/api/inventory-sds-record-for-product/" + product_id + "/";
      console.log("Url get sds record details : " + URL_GET_SDS_DETAILS);
  
      $.ajax({
        type: "GET",
        url: URL_GET_SDS_DETAILS,
        beforeSend: function (xhr) {
          xhr.setRequestHeader("Authorization", token_string);
        },
        success: function (json_data) {
          // alert(json_data);
          if (json_data["success"] === true) {
            console.log(json_data["data"]);
            $("#sds-name").val(json_data["data"]["SDSNameURL"]);
  
            $("#sds-cas-num").val(json_data["data"]["SDSCasNo"]);
  
            $("#sds-component").val(json_data["data"]["SDSComponent"]);
  
            $("#sds-url").val(json_data["data"]["SDSLocationURL"]);
          }
        },
        error: function (json_data) {
          console.log("ERROR Sds Record");
        },
      });
    }
  
    // Adding evene listener to Add Transaction Button
    var add_transaction_btn = document.querySelector("#st-add-transaction-btn");
    add_transaction_btn.addEventListener("click", () => {
      // console.log("Add Transaction Button Clicked");
      if (!current_selected_product) {
        // show toast to select a product
        showToast("No product selected", (type = "warning"));
      } else if (st_input_active === true) {
        // pass
      } else {
        st_input_active = true;
        st_in_selected = false;
        st_out_selected = false;
  
        var st_table_body = document.querySelector("#st-table-body");
  
        var table_row = document.createElement("tr");
  
        table_row.setAttribute("id", "add-new-sds-transaction");
        table_row.setAttribute("class", "st-table-row");
  
        // td - date
        var td_date = $(document.createElement("td"));
        $(td_date).html(
          '<input type="date" id="st-date-input" name="st-date-input" class="st-inputs">'
        );
  
        $(table_row).append(td_date);
  
        // td - calander icon in a link
        var td_calander = $(document.createElement("td"));
  
        var td_calender_a = $(document.createElement("a")).prop({
          class: "dropdown-toggle waves-effect waves-light font-20",
        });
        $(td_calender_a).attr("data-toggle", "dropdown");
  
        var td_calender_i = $(document.createElement("i")).prop({
          class: "fa-regular fa-calendar-days",
        });
  
        $(td_calender_a.append(td_calender_i));
        $(td_calander).append(td_calender_a);
        $(table_row).append(td_calander);
  
        $(st_table_body).prepend(table_row);
  
        // td- Lot Number
        var td_lot_number = $(document.createElement("td"));
        $(td_lot_number).html(
          '<input type="text" id="st-lot-input" name="st-lot-input" placeholder="Lot" class="st-inputs">'
        );
        $(table_row).append(td_lot_number);
  
        // td- Description
        var td_description = $(document.createElement("td"));
        $(td_description).html(current_selected_product["ItemName"]);
        $(table_row).append(td_description);
        console.log(current_selected_product);
  
        // td - Units in a link
        var td_units = $(document.createElement("td")).prop({
          class: "text-nowrap",
        });
  
        var td_units_a = $(document.createElement("a"));
        $(td_units_a).attr("data-toggle", "tooltip");
        $(td_units_a).attr("data-original-title", "Edit");
  
        $(td_units).append(td_units_a);
        $(td_units).append(
          '<input type="text" id="st-units-input" name="st-units-input" placeholder="Units" class="st-inputs">'
        );
        $(table_row).append(td_units);
  
        // td - units_measure in a link
        var td_units_measure = $(document.createElement("td")).prop({
          class: "text-nowrap",
        });
  
        var td_units_measure_a = $(document.createElement("a"));
        $(td_units_measure_a).attr("data-toggle", "tooltip");
        $(td_units_measure_a).attr("data-original-title", "Edit");
  
        $(td_units_measure).append(td_units_measure_a);
        $(td_units_measure).append(
          '<input type="text" id="st-unit-measure-input" name="st-unit-measure-input" placeholder="UM" class="st-inputs">'
        );
        $(table_row).append(td_units_measure);
  
        // td - buttons in a link
        var td_buttons = $(document.createElement("td")).prop({
          class: "text-nowrap",
        });
  
        var td_buttons_a = $(document.createElement("a"));
        $(td_units_a).attr("data-toggle", "tooltip");
        $(td_units_a).attr("data-original-title", "Close");
  
        var td_buttons_div = $(document.createElement("div")).prop({
          class: "btn-group",
        });
  
        var td_button_in = $(document.createElement("button")).prop({
          class: "btn btn-default btn-outline waves-effect",
          type: "button",
          id: "add-new-st-in-button",
        });
        $(td_button_in).html("In");
  
        var td_button_out = $(document.createElement("button")).prop({
          class: "btn btn-default btn-outline waves-effect",
          type: "button",
          id: "add-new-st-out-button",
        });
        $(td_button_out).html("Out");
  
        $(td_buttons_div).append(td_button_in);
        $(td_buttons_div).append(td_button_out);
        $(td_buttons_a).append(td_buttons_div);
        $(td_buttons).append(td_buttons_a);
        $(table_row).append(td_buttons);
  
        // td - go button in a link
        var td_go_btn = $(document.createElement("td")).prop({
          class: "text-nowrap",
        });
  
        var td_go_btn_a = $(document.createElement("a")).prop({
          class: "dropdown-toggle waves-effect waves-light font-20 st-go-button",
          href: "javascript:void(0);",
          id: "add-new-st-go-button",
        });
        $(td_go_btn_a).attr("data-toggle", "dropdown");
  
        var td_go_btn_i = $(document.createElement("i")).prop({
          class: "fa-solid fa-play",
        });
  
        $(td_go_btn_a).append(td_go_btn_i);
        $(td_go_btn).append(td_go_btn_a);
        $(table_row).append(td_go_btn);
  
        // td - cancel button in a link
        var td_cancel_btn = $(document.createElement("td")).prop({
          class: "text-nowrap",
        });
  
        var td_cancel_btn_a = $(document.createElement("a")).prop({
          class:
            "dropdown-toggle waves-effect waves-light font-20 st-cancel-button",
          href: "javascript:void(0);",
          id: "add-new-st-cancel-button",
        });
        $(td_cancel_btn_a).attr("data-toggle", "dropdown");
  
        var td_cancel_btn_i = $(document.createElement("i")).prop({
          class: "fa-solid fa-xmark",
        });
  
        $(td_cancel_btn_a).append(td_cancel_btn_i);
        $(td_cancel_btn).append(td_cancel_btn_a);
        $(table_row).append(td_cancel_btn);
  
        st_table_body.prepend(table_row);
  
        addEventListenerToAddNewStTableRow();
      }
    });
  
    function addEventListenerToAddNewStTableRow() {
      var in_btn = document.querySelector("#add-new-st-in-button");
      var out_btn = document.querySelector("#add-new-st-out-button");
  
      in_btn.addEventListener("click", function () {
        st_in_selected = true;
        st_out_selected = false;
  
        in_btn.classList.add("active-yellow-button");
        out_btn.classList.remove("active-yellow-button");
      });
  
      out_btn.addEventListener("click", function () {
        st_in_selected = false;
        st_out_selected = true;
  
        in_btn.classList.remove("active-yellow-button");
        out_btn.classList.add("active-yellow-button");
      });
  
      var cancel_button = document.querySelector("#add-new-st-cancel-button");
      cancel_button.addEventListener("click", function () {
        var st_table_body = document.querySelector("#st-table-body");
        st_table_body.removeChild(
          document.querySelector("#add-new-sds-transaction")
        );
        st_input_active = false;
      });
  
      var go_button = document.querySelector("#add-new-st-go-button");
      go_button.addEventListener("click", function () {
        var units = document.querySelector("#st-units-input").value;
        var product_id = current_selected_product["id"];
        var unit_measure = document.querySelector("#st-unit-measure-input").value;
        var date = document.querySelector("#st-date-input").value;
        var lot_number = document.querySelector("#st-lot-input").value;
        var user = 0;
  
        var selected_in_or_out_button;
        if (st_in_selected) {
          selected_in_or_out_button = "in";
        } else if (st_out_selected) {
          selected_in_or_out_button = "out";
        }
  
        postNewStockTransaction(
          (units = units),
          (product_id = product_id),
          (unit_measure = unit_measure),
          (lot_number = lot_number),
          (user = user),
          (date = date),
          (selected_in_or_out = selected_in_or_out_button)
        );
      });
    }
  
    function postNewStockTransaction(
      units,
      product_id,
      unit_measure,
      lot_number,
      user,
      date,
      selected_in_or_out
    ) {
      // alert("Posting new St");
  
      let URL_POST_STOCK_TRANSACTION;
      if (selected_in_or_out === "in") {
        URL_POST_STOCK_TRANSACTION = "/api/post-inventory-stock-transaction/in/";
      } else if (selected_in_or_out === "out") {
        URL_POST_STOCK_TRANSACTION = "/api/post-inventory-stock-transaction/out/";
      }
  
      console.log(
        "Url post stock transaction (in/out) : " + URL_POST_STOCK_TRANSACTION
      );
      var formdata = {
        units: parseFloat(units),
        product_id: product_id,
        unit_measure: unit_measure,
        lot_number: lot_number,
        date: date,
        user: user,
      };
  
      $.ajax({
        type: "POST",
        url: URL_POST_STOCK_TRANSACTION,
        data: formdata,
        beforeSend: function (xhr) {
          xhr.setRequestHeader("Authorization", token_string);
        },
        success: function (json_data) {
          // alert(json_data);
          if (json_data["success"] === true) {
            console.log(json_data["data"]);
            showToast("Stock Transaction added successfully", (type = "success"));
            getAllStockTransactionsAndAppend(current_selected_product["id"]);
          }
        },
        error: function (json_data) {
          console.log("ERROR POST STOCK TRANSACTION IN/OUT");
        },
      });
    }
  
    var next_product_select_btn = document.querySelector(
      "#next-product-select-btn"
    );
    next_product_select_btn.addEventListener("click", () => {
      selectNextOrPreviousProduct("next");
    });
  
    var previous_product_select_btn = document.querySelector(
      "#previous-product-select-btn"
    );
    previous_product_select_btn.addEventListener("click", () => {
      selectNextOrPreviousProduct("previous");
    });
  
    function selectNextOrPreviousProduct(selector) {
      var product_btn_container = document.querySelector(
        "#product-buttons-container"
      );
      var next_active_btn;
      var first_btn;
      var active_btn;
      var prev_btn;
  
      if (selector === "next") {
        next_active_btn = document.querySelector(
          "#product-buttons-container .active-button + button"
        );
  
        if (next_active_btn) {
          $(next_active_btn).trigger("click");
        } else {
          first_btn = document.querySelector("#product-buttons-container button");
          // select the first elem in product_btn_container
          if (first_btn) {
            $(first_btn).trigger("click");
          } else {
            // show a toast that no products exists
          }
        }
      } else if (selector === "previous") {
        active_btn = document.querySelector(
          "#product-buttons-container .active-button"
        );
  
        if (active_btn) {
          prev_btn = active_btn.previousSibling;
          $(prev_btn).trigger("click");
        } else {
          first_btn = document.querySelector("#product-buttons-container button");
          // select the first elem in product_btn_container
          if (first_btn) {
            $(first_btn).trigger("click");
          } else {
            // show a toast that no products exists
          }
        }
      }
    }
  
    // go to new product entry form
    var new_edit_btn = document.querySelector("#new-product-entry-btn");
    new_edit_btn.addEventListener("click", () => {
      // alert("clicked");
      window.location.href = "//" + URL_NEW_PRODUCT_ENTRY_FORM;
    });
  
    // go to list page
    var list_page_btn = document.querySelector("#list-page-btn");
    list_page_btn.addEventListener("click", () => {
      // alert("clicked");
      window.location.href = "//" + URL_LIST_PAGE;
    });
  
    // Get products in asc order
    var sort_asc = document.querySelector("#sort-btn-asc");
    sort_asc.addEventListener("click", () => {
      // alert("clicked");
      selected_sort = "asc";
      get_products_and_fill_list(
        last_used_filter_category,
        last_used_filter_category_value,
        "asc"
      );
    });
  
    // Get products in dec order
    var sort_dec = document.querySelector("#sort-btn-dec");
    sort_dec.addEventListener("click", () => {
      // alert("clicked");
      selected_sort = "dec";
      get_products_and_fill_list(
        last_used_filter_category,
        last_used_filter_category_value,
        "dec"
      );
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
  
    var add_units_measure_form_a = document.querySelector(
      "#add-units-measure-form-a"
    );
    add_units_measure_form_a.addEventListener("click", () => {
      // alert("clicked");
      window.location.href = "//" + URL_ADD_UNITS_MEASURE_FORM;
    });
  
    // Get products in dec order
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
  
    // Add event listener of delete button
    var del_btn = document.querySelector("#product-delete-btn");
    del_btn.addEventListener("click", () => {
      if (current_selected_product === null) {
        showToast("No entry selected", "warning");
      } else {
        swal({
          title: "Are you sure?",
          text: "Delete the entry",
          icon: "warning",
          buttons: true,
          dangerMode: true,
        }).then((willDelete) => {
          if (willDelete) {
            // deleteStockTransactionAndRefreshTable(stock_transaction_id, product_id);
            let URL_DELETE_INVENTORY =
              URL_BASE_DELETE_INVENTORY + current_selected_product["id"] + "/";
            current_selected_product = null;
            console.log("DELETIING NOW");
            console.log("DELETIING NOW URL " + URL_DELETE_INVENTORY);
  
            $.ajax({
              type: "POST",
              url: URL_DELETE_INVENTORY,
              beforeSend: function (xhr) {
                xhr.setRequestHeader("Authorization", token_string);
              },
              success: function (json_data) {
                if (json_data["success"] === true) {
                  var name = $("#search-list-entries").val();
                  $("#list-item-name").val("");
                  get_products_and_fill_list(
                    (search_by = last_used_filter_category),
                    (search = last_used_filter_category_value),
                    (sort = selected_sort)
                  );
                  showToast("Entry successfully deleted", (type = "success"));
                  // TODO: Make a reset form function
                  document.getElementById("main-product-form").reset();
                  document.getElementById("product-name-heading").innerHTML = "Select Product..";
                  
  
                  // var first_btn = document.querySelector("#product-buttons-container button");
                  // // select the first elem in product_btn_container
                  // if (first_btn) {
                  //   $(first_btn).trigger("click");
                  // }
                  // else{
                  //   // reset form
                  // }
                }
              },
              error: function (json_data) {
                console.log("ERROR Delete List Item");
              },
            });
          } else {
          }
        });
      }
    });
  
    // var this_btn = document.querySelector("#this-button");
    // this_btn.addEventListener("click", ()=>{
    //   clickedOnThis();
    // });
  
    function getGroupsAndShowInSearchBox(group_name) {
      var URL_GET_ALL_GROUPS = "api/get-all-groups/?name=" + group_name;
      $.ajax({
        type: "GET",
        url: URL_GET_ALL_GROUPS,
        beforeSend: function (xhr) {
          xhr.setRequestHeader("Authorization", token_string);
        },
        success: function (json_data) {
          // alert(json_data);
          if (json_data["success"] === true) {
            console.log(json_data["data"]);
          }
        },
        error: function (json_data) {
          console.log("ERROR Getting groups");
        },
      });
    }
  
    function clickedOnThis() {
      alert("RUNNING");
      var s = document.getElementById("categories-options");
      s.selectedIndex = 0;
      get_products_and_fill_list("groups", "1");
    }
  
    // Group Search Bar
    var group_search_input = document.querySelector("#group-search-input");
    group_search_input.addEventListener("focusin", () => {
      // alert("focusin");
      var input_field = document.querySelector("#group-search-input");
      fillGroupsSuggestionDiv((input_value = input_field.value));
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
  
    // Group search bar END
  
    // Add event listener to fields to update them
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
  });
  