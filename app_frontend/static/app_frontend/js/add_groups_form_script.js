$(document).ready(function () {
  // alert("ayo");
  let currently_selected_list_item = null;
  var BASE_URL = "127.0.0.1:8000";
  var URL_GET_ALL_GROUPS = "/api/get-all-groups/";
  var URL_BASE_GET_GROUP_DETAILS = "/api/get-group-details/";
  var URL_BASE_UPDATE_GROUP = "/api/update-group/";
  var URL_POST_NEW_GROUP = "/api/create-group/";
  var URL_BASE_DELETE_GROUP = "/api/delete-group/";
  var sorting = "asc";

  var token = window.localStorage.getItem("token");

  if (!token) {
    // redirect to login page
    // console.log("token" + token);
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

  function get_list_items_and_fill_list(search_name="", sort="asc") {
    
    $.ajax({
      type: "GET",
      url: URL_GET_ALL_GROUPS+ "?sort=" + sort + "&name=" + search_name,
      beforeSend: function (xhr) {
        xhr.setRequestHeader("Authorization", token_string);
      },
      success: function (json_data) {
        // alert(json_data);
        if (json_data["success"] === true) {
          // console.log(json_data["data"]);
          if(json_data["data"]["count"] === 0){
            $(".buttons-container").html("<p id='no-entries-p'>No entries</p>");
          }
          else{
            $(".buttons-container").html("");
            for (let i = 0; i < json_data["data"]["count"]; i++) {
              var list_button = $(document.createElement("button")).prop({
                type: "button",
                innerHTML: json_data["data"]["list"][i]["name"],
                id: json_data["data"]["list"][i]["id"],
                class: "list-button",
              });
              $(list_button).css(
                { 
                  "text-align": "left", 
                  "padding": "6px", 
                  "overflow": "hidden", 
                  "text-overflow": "ellipsis", 
                  "white-space": "nowrap"
                }
              );
              $(".buttons-container").append(list_button);
            }
            add_event_listener_to_buttons();
          }
          
        }
      },
      error: function (json_data) {
        console.log("ERROR Get ALl List Items");
      },
    });
  }

  get_list_items_and_fill_list();

  // Adding event listener in buttons and calling the fill product details on button click
  function add_event_listener_to_buttons() {
    // alert("Button  listener is being added");
    let buttons = document.querySelectorAll(".list-button");
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
        getListItemDetailsAndFillFormData(item.id);
      });
    });
  }

  function getListItemDetailsAndFillFormData(id) {
    let URL_GET_GROUP_DETAILS = URL_BASE_GET_GROUP_DETAILS + id + "/";
    $.ajax({
      type: "GET",
      url: URL_GET_GROUP_DETAILS,
      beforeSend: function (xhr) {
        xhr.setRequestHeader("Authorization", token_string);
      },
      success: function (json_data) {
        // alert(json_data);
        currently_selected_list_item = json_data["data"];
        if (json_data["success"] === true) {
          $("#list-item-name").val(json_data["data"]["name"]);
          0;
          edit_btn.style.display = "block";
          save_btn.style.display = "none";
          cancel_btn.style.display = "none";
          $("#list-item-name").attr("readonly", true);
        
        }
      },
      error: function (json_data) {
        console.log("ERROR Get List Item Details");
      },
    });
  }

  // buttons
  var cancel_btn = document.querySelector("#cancel-btn");
  var save_btn = document.querySelector("#save-btn");
  var edit_btn = document.querySelector("#edit-btn");

  // Event listener on cancel btn
  cancel_btn.addEventListener("click", () => {
    edit_btn.style.display = "block";
    save_btn.style.display = "none";
    cancel_btn.style.display = "none";
    $("#list-item-name").attr("readonly", true);
    $("#list-item-name").val(currently_selected_list_item["name"]);
  });

  // Event listener on edit btn
  edit_btn.addEventListener("click", () => {
    if (currently_selected_list_item === null) {
      showToast("No entry selected", "warning");
      return;
    }
    edit_btn.style.display = "none";
    save_btn.style.display = "block";
    cancel_btn.style.display = "block";
    $("#list-item-name").attr("readonly", false);
  });

  // Event listener on cancel btn
  save_btn.addEventListener("click", () => {
    let URL_UPDATE_GROUP =
      URL_BASE_UPDATE_GROUP + currently_selected_list_item["id"] + "/";
    var form_data = {
      name: $("#list-item-name").val(),
    };

    $.ajax({
      type: "POST",
      url: URL_UPDATE_GROUP,
      data: form_data,
      beforeSend: function (xhr) {
        xhr.setRequestHeader("Authorization", token_string);
      },
      success: function (json_data) {
        // alert(json_data);

        if (json_data["success"] === true) {
          // alert("here");
          $("#list-item-name").val(json_data["data"]["name"]);
          current_selected_product = json_data["data"];
          edit_btn.style.display = "block";
          save_btn.style.display = "none";
          cancel_btn.style.display = "none";
          $("#list-item-name").attr("readonly", true);
          document.querySelector(".active-button").innerHTML =
            current_selected_product["name"];
          showToast("Entry successfully updated", "success");
        }
      },
      error: function (json_data) {
        console.log("ERROR Update List Item Details");
      },
    });
  });

  var add_new_list_item = document.querySelector("#add-new-list-item");
  add_new_list_item.addEventListener("click", () => {
    if (
      $("#list-item-name-input").val() === null ||
      $("#list-item-name-input").val() === ""
    ) {
      showToast("You must provide a value", "warning");
    }
    // const formData = new FormData();
    // formData.append("name", $("#list-item-name-input").val());

    var form_data = {
      name: $("#list-item-name-input").val(),
    };

    $.ajax({
      type: "POST",
      url: URL_POST_NEW_GROUP,
      data: form_data,
      beforeSend: function (xhr) {
        xhr.setRequestHeader("Authorization", token_string);
      },
      success: function (json_data) {
        // alert(json_data);

        if (json_data["success"] === true) {
          // alert("here");
          get_list_items_and_fill_list();
          currently_selected_list_item = null;
          edit_btn.style.display = "block";
          save_btn.style.display = "none";
          cancel_btn.style.display = "none";
          $("#list-item-name").attr("readonly", true);
          $("#list-item-name").val("");
          $("#list-item-name-input").val("");
          showToast("New entry added successfully", "success");
        }
      },
      error: function (json_data) {
        console.log("ERROR Update List Item Details");
      },
    });
  });

  // home-btn
  var home_btn = document.querySelector("#home-btn");
  home_btn.addEventListener("click", () => {
    window.location.href = "//" + BASE_URL;
  });

  var next_item_select_btn = document.querySelector("#next-item-select-btn");
  next_item_select_btn.addEventListener("click", () => {
    selectNextOrPreviousProduct("next");
  });

  var previous_item_select_btn = document.querySelector(
    "#previous-item-select-btn"
  );
  previous_item_select_btn.addEventListener("click", () => {
    selectNextOrPreviousProduct("previous");
  });

  function selectNextOrPreviousProduct(selector) {
    var product_btn_container = document.querySelector(
      "#list-items-buttons-container"
    );
    var next_active_btn;
    var first_btn;
    var active_btn;
    var prev_btn;

    if (selector === "next") {
      next_active_btn = document.querySelector(
        "#list-items-buttons-container .active-button + button"
      );

      if (next_active_btn) {
        $(next_active_btn).trigger("click");
      } else {
        first_btn = document.querySelector(
          "#list-items-buttons-container button"
        );
        // select the first elem in product_btn_container
        if (first_btn) {
          $(first_btn).trigger("click");
        } else {
          // show a toast that no products exists
        }
      }
    } else if (selector === "previous") {
      active_btn = document.querySelector(
        "#list-items-buttons-container .active-button"
      );

      if (active_btn) {
        prev_btn = active_btn.previousSibling;
        $(prev_btn).trigger("click");
      } else {
        first_btn = document.querySelector(
          "#list-items-buttons-container button"
        );
        // select the first elem in product_btn_container
        if (first_btn) {
          $(first_btn).trigger("click");
        } else {
          // show a toast that no products exists
        }
      }
    }
  }

  // Get products in asc order
  var sort_asc = document.querySelector("#sort-btn-asc");
  sort_asc.addEventListener("click", () => {
    // alert("clicked");
    sorting = "asc";
    var name = $('#search-list-entries').val();
    get_list_items_and_fill_list(search_name=name, sort="asc");
  });

  // Get products in dec order
  var sort_dec = document.querySelector("#sort-btn-dec");
  sort_dec.addEventListener("click", () => {
    sorting = "dec";
    var name = $('#search-list-entries').val();
    get_list_items_and_fill_list(search_name=name, sort="dec");
  });

  // Add event listener of delete button
  var del_btn = document.querySelector("#list-item-delete-btn");
  del_btn.addEventListener("click", ()=>{
    if (currently_selected_list_item === null){
      showToast("No entry selected", "warning");
    }
    else{
      swal({
        title: "Are you sure?",
        text: "Delete the entry",
        icon: "warning",
        buttons: true,
        dangerMode: true,
      })
      .then((willDelete) => {
        if (willDelete) {
          // deleteStockTransactionAndRefreshTable(stock_transaction_id, product_id);
          let URL_DELETE_GROUP = URL_BASE_DELETE_GROUP + currently_selected_list_item["id"] + "/";
          currently_selected_list_item = null;

          $.ajax({
            type: "POST",
            url: URL_DELETE_GROUP,
            beforeSend: function (xhr) {
              xhr.setRequestHeader("Authorization", token_string);
            },
            success: function (json_data) {
              if (json_data["success"] === true) {
                var name = $('#search-list-entries').val();
                $("#list-item-name").val("");
                get_list_items_and_fill_list(search_name=name, sort=sorting);
                showToast("Entry successfully deleted", type="success");
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

  })

  // Event Listener on search field
  var search_field = document.querySelector("#search-list-entries");
  search_field.addEventListener("keyup", ()=>{
    var name = $('#search-list-entries').val();
    get_list_items_and_fill_list(search_name=name, sort=sorting);
  });
  
});
