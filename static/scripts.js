var signup = document.getElementById('register-form');
var signin = document.getElementById('login-form');
var alertMsg = document.querySelector('#alert');
var alertMsg2 = document.querySelector('#alert2');
var alertCPMsg = document.querySelector('#alert_change_psw');
var alertDeleteMsg = document.querySelector('#alertDelete');
var alertMsgAvatar = document.querySelector('#avatar-alert');
var alertText = document.querySelector('#alert p');
var alertDash = document.querySelector('#alertDash');
var alertDashText = document.querySelector('#alertDash p');
var logout = document.getElementById('logout-btn');
var profileUpdate = document.getElementById('profile-update');
var changePasswordUpdate = document.getElementById('change-password-update');
var uploadAvatar = document.getElementById('avatar-upload-form'); 
var passswordReset = document.getElementById('password-rest-form');
var passswordConfirm = document.getElementById('password-rest-confirm');
var post_form = document.getElementById('post-form');
var like_post = document.getElementById('like-post');
var spinner = document.getElementById('js-preloader');
var spinner2 = document.getElementById('ajax-loader');
var span = document.getElementById('span');
var togglePassword = document.querySelector('#togglePassword');

function alertMessage(bg,msg,selector) {
    selector.innerHTML += `<div class="alert ${bg} text-white alert-dismissible fade show" role="alert">
                                <div class="d-flex justify-content-between">
                                    <p class="p-1">${msg}</p>
                                    <button type="button" class="close m-2" data-dismiss="alert" aria-label="Close">
                                        <span aria-hidden="true">&times;</span>
                                    </button>	
                                    </div>											
                            </div>`
}

//TogglePassword
function myFunctionToggle() {
    var password = document.querySelector('#password');
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    togglePassword.classList.toggle('fa-eye-slash');
}

//TogglePassword
function myFunctionToggleSignin(psd, toggled_id) {
    var password = document.querySelector("#"+psd);
    var togglePsd = document.querySelector("#"+toggled_id);
    var type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    togglePsd.classList.toggle('fa-eye-slash');
}

// Toggled Changed Password
function changePasswordToggled(psd, toggled_id) {
    var password = document.querySelector("#"+psd);
    var togglePsd = document.querySelector("#"+toggled_id);
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    password.setAttribute('type', type);
    togglePsd.classList.toggle('fa-eye-slash');
}

//TitleCase
String.prototype.toProperCase = function () {
    return this.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
};

var getCookie = function(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

var csrftoken = getCookie('csrftoken');

//Sign Up User
if (signup) {
    signup.addEventListener('submit', function(event) {
        event.preventDefault();
        let form = document.getElementById('register-form');
        let email = document.getElementById('email');
        let password = document.getElementById('password');
        let password2 = document.getElementById('compsd');
        let first_name = document.getElementById('first_name');
        let last_name = document.getElementById('last_name');
        let gender = document.getElementById('gender');
        let contact = document.getElementById('contact');
        let dob = document.getElementById('dob');
        let pattern = /^\b[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b$/i

        var newData =   {
            "email": email.value,
            "password": password.value,
            "first_name": first_name.value.toProperCase(),
            "last_name": last_name.value.toProperCase(),
            "gender": gender.value,
            "contact": contact.value,
            "dob": dob.value
        };

        var dataJson = JSON.stringify(newData);
        console.log(dataJson);
        if (password.value != password2.value) {
            alertMessage("bg-danger","Password does not match!", alertMsg);
        } else if (password.value.length < 8) {
            alertMessage("bg-danger","Password must not be less than 8 characters", alertMsg);
        } else if (!pattern.test(email.value)) {
            alertMessage("bg-danger","Invalid Email", alertMsg);
        } else {
            $.ajax({
                type: "POST",
                beforeSend: function() {
                    spinner.style.visibility = 'visible';
                },        
                url: "/api/user/register/",        
                data: dataJson,  
                success: function(result) {
                    console.log(result);
                    document.title = "Registered Student";
                    alertMessage("bg-success","Registered Successfully! Please Signin.",alertMsg)
                    form.reset();

                },
                error: function (xhr, status, error) {
                    err = xhr.responseText.split("\"")[3].replace(/"|'/g,);
                    if (xhr["status"] === 400) {
                        alertMessage("bg-danger",`${err}`,alertMsg);
                    }                    
                    if (xhr["status"] === 500) {
                        alertMessage("bg-danger","Internal Server Error!",alertMsg);
                    }
                },
                complete: function() {
                    spinner.style.visibility = 'hidden';
                },
                dataType: "json",
                contentType: "application/json"
            });  
        }        
    });
};


//Sign In User
if (signin) {
    signin.addEventListener('submit', function(event) {
        event.preventDefault();
        let form = document.getElementById('login-form');
        let email = document.getElementById('email1');
        let password = document.getElementById('password1'); 
        
        var newData = {
            "email": email.value,
            "password": password.value
        };      

        var dataJson = JSON.stringify(newData);
        console.log(dataJson);

        $.ajax({
            type: "POST",
            beforeSend: function() {
                spinner2.style.visibility = 'visible';
            },        
            url: "/api/user/login/",
            headers: {
                'X-CSRFToken': csrftoken,
            },
            data: dataJson,
            success: function(result) {
                console.log(result);
                console.log(result.token);
                document.querySelector('title').textContent = "Home Page";
                if (result['success'] == "True") {
                    window.location.href = `${window.location.origin}/posts`;
                    // alert("User Login succefully!");                        
                } else if (result['success'] == "False") {
                    spinner2.style.visibility = 'hidden';
                    alertMessage("bg-danger",result['message'], alertMsg2);
                } else {
                    window.location.href
                }                
                form.reset();
            },
            error: function (error) {
                if (error['status'] === 500) {
                    alertMessage("bg-danger",`${error["statusText"]}`, alertMsg2)
                }
                else if (error['status'] === 400) {
                //    console.log(error.responseJSON);
                    console.log(error["responseJSON"]);
                    if (error["responseJSON"] && error["responseJSON"]['status'] === "False") {
                        alertMessage("bg-danger",`${error["responseJSON"]["message"]}`, alertMsg2);
                    }                    
                }               
                                                    
            },
            complete: function(){
                spinner2.style.visibility = 'hidden';
            },
            dataType: "json",
            contentType: "application/json"
        });
    });
}


// Upload User Avatar
if (uploadAvatar) {
    uploadAvatar.addEventListener('submit', function(event) {
        event.preventDefault();
        let form = document.getElementById('avatar-upload-form');
        let imageTag = document.getElementsByTagName('IMG');
        let input = document.getElementById('id_avatar');
        let data_img = new FormData();
        data_img.append('avatar', input.files[0], input.files[0].name);

        if ( /\.(jpe?g|png|gif)$/i.test(input.files[0].name) === false) { 
            //Validating the Image Type
            alertMessage('bg-danger','image must be jpg/png/gif!', alertMsgAvatar); 
        } else if (input.files[0].size > 1048576) {
            alertMessage('bg-danger','Image file larger than 1MB!', alertMsgAvatar);
        } else {
            $.ajax({
                type: "POST",
                beforeSend: function() {
                    spinner.style.visibility = 'visible';
                },   
                url: "/api/user/avatar/",
                headers: {
                    'X-CSRFToken': csrftoken,
                },
                contentType: false,
                processData: false,
                data: data_img,
                success: function(result) {
                    console.log("result *************", result['avatar']);
                    imageTag.src = result['avatar'];
                    document.title = "Avatar Uploaded";              
                    alertMessage('bg-success','Avatar Uploaded Successfully!',alertMsgAvatar);
                    // console.log(input.files[0].size);
                },
                error: function (error) {
                    console.log(error);
                    console.log(error["responseJSON"]["detail"]);
                    alertMessage('bg-danger','Avatar not uploaded!', alertMsgAvatar);
                    if (error.status === 500) alertMessage('bg-danger','Server Error!', alertMsgAvatar);
                },
                complete: function(){
                    spinner.style.visibility = 'hidden';
                },
            });            
        }
        form.reset();        
    });   
}


//Logout User
function logoutNow() {
    $.ajax({
        type: "POST",
        beforeSend: function() {
            spinner.style.visibility = 'visible';
        },   
        url: "/api/user/logout/",
        headers: {
            'X-CSRFToken': csrftoken,
        },
        success: function(result) {
            console.log(result);
            redirect_path = `${window.location.origin}`
            window.location.href = redirect_path
        },
        error: function (error) {
            console.log(error);
            console.log(error["responseText"]);
            console.log(error["responseJSON"]["detail"]);
        },
        complete: function(){
            spinner.style.visibility = 'hidden';
        },
        dataType: "json",
        contentType: "application/json"
    });
}


//Reset Password
if (passswordConfirm) {
    passswordConfirm.addEventListener('submit', function(event) {
        event.preventDefault();
        let form = document.getElementById('password-rest-confirm');
        let password = document.getElementById('password');
        let con_password = document.getElementById('con_password');
        let token = document.getElementById('token');
            
        var newData = {
            "password": password.value,
            "token": token.value
        };

        var dataJson = JSON.stringify(newData);
        console.log(dataJson);
        if (password.value != con_password.value) {
            alertMessage("bg-danger","Password does not match!",alertMsg)
        } else {
            $.ajax({
                type: "POST", 
                beforeSend: function() {
                    spinner.style.visibility = 'visible';
                },   
                url: "/api/user/password/update/",
                headers: {
                    'X-CSRFToken': csrftoken,
                },
                data: dataJson,
                success: function(result) {
                    console.log(result);
                    alertMessage("bg-success","Password reset successfully!",alertMsg)
                },
                error: function (error) {
                    console.log(error);
                    if (error["responseJSON"]["password"][0]) {
                        alertMessage("bg-danger",`${error["responseJSON"]["password"][0]}`,alertMsg); 
                    } else {
                       alertMessage("bg-danger","Password reset unsuccessfully!",alertMsg) 
                    }                    
                },
                complete: function(){
                    spinner.style.visibility = 'hidden';
                },
                dataType: "json",
                contentType: "application/json"
            });    
        }        
        form.reset();
	});
}


// Change Password
if (changePasswordUpdate) {
    changePasswordUpdate.addEventListener('submit', function(event) {
        event.preventDefault();
        let form = document.getElementById('change-password-update');
        let old_password = document.getElementById('old_password');
        let new_password = document.getElementById('new_password');
        let confirm_password = document.getElementById('confirm_password');            
        var newData = {
            "old_password": old_password.value,
            "password": new_password.value,
            "password2": confirm_password.value        
        };
        var dataJson = JSON.stringify(newData);

        if (new_password.value !== confirm_password.value) {
            alertMessage("bg-danger","Password fields didn't match.", alertCPMsg);
        } else {
            $.ajax({
                type: "PUT",
                beforeSend: function() {
                    spinner.style.visibility = 'visible';
                },     
                url: "/api/user/password/update/",
                headers: {
                    'X-CSRFToken': csrftoken,
                },
                data: dataJson,
                success: function(result) {
                    // alert("Password Updated Successfully!")
                    alertMessage("bg-success","Password Updated Successfully!", alertCPMsg);
                    form.reset() 
                    window.location.href = `${window.location.origin}`;
                },
                error: function (error) {
                    console.log(error);
                    console.log(error["responseText"]);
                    if (error["responseJSON"]["old_password"][0]) {
                        alertMessage("bg-danger",`${error["responseJSON"]["old_password"][0]}`, alertCPMsg);
                    }
                    form.reset()
                },
                complete: function(){
                    spinner.style.visibility = 'hidden';
                },
                dataType: "json",
                contentType: "application/json"
            });    
        }
    });   
}


//Update Profile
if (profileUpdate) {
    profileUpdate.addEventListener('submit', function(event) {
        event.preventDefault();
        let first_name = document.getElementById('first_name');
        let last_name = document.getElementById('last_name')
        let gender = document.getElementById('gender');
        let contact = document.getElementById('contact'); 
        let dob = document.getElementById('dob');
        var newData = {
            "first_name": first_name.value.toProperCase(),
            "last_name": last_name.value.toProperCase(),
            "gender": gender.value,
            "contact": contact.value,
            "dob": dob.value,
        };
        var dataJson = JSON.stringify(newData);
        console.log(dataJson)
        $.ajax({
            type: "PUT",
            beforeSend: function() {
                spinner.style.visibility = 'visible';
            },  
            url: "/api/user/profile/update/",
            headers: {
                'X-CSRFToken': csrftoken,
            },
            data: dataJson,
            success: function(result) {
                // alert("Profile Updated Updated Successfully!")
                alertMessage("bg-success","Profile Updated Successfully!", alertMsg);
            },
            error: function (error) {
                console.log(error);
                if (error["responseJSON"]["old_password"][0]) {
                    alertMessage("bg-danger",`${error["responseJSON"]["old_password"][0]}`, alertMsg); 
                }
            },
            complete: function(){
                spinner.style.visibility = 'hidden';
            },
            dataType: "json",
            contentType: "application/json"
        });
    });   
}

// POST
var img_wrapper = $('.img-display-wrapper')
var video_wrapper = $('.video-display-wrapper')
var img_source = $('#postmodal .modal-body #image-display');
var video_source = $('#video-display');
// Initially
img_wrapper.css('display','None');
video_wrapper.css('display','None');


 // VIDEO UPLOAD
 $('#video-upload-btn').on('change', function() {
    img_wrapper.css('display','None');
    video_wrapper.css('display','flex');
    img_source.attr('src','');
    video_source[0].src = URL.createObjectURL(this.files[0]);
    video_source.parent()[0].load();
})

 // IMAGE UPLOAD 
 $('#image-upload-btn').on('change', function() {
    img_wrapper.css('display','flex');
    video_wrapper.css('display','None');
    // video_source[0].src = ''
    video_source.parent()[0].load();
    if (this.files && this.files[0]) {       
       img_source[0].src = URL.createObjectURL(this.files[0]); 
    }    
})

// Reset From on Post Modal Close
$("#postmodalclose-btn").on('click', function() {
    $("#post-form").trigger("reset");
    $("input[type=file]").val(null)
    img_source.attr('src','');
    video_source[0].src = ''
    video_source.parent()[0].load();
    img_wrapper.css('display','None');
    video_wrapper.css('display','None');
});


if (post_form) {
    post_form.addEventListener('submit', function(event) {
        event.preventDefault();
        let form = document.getElementById('post-form');
        let text = document.getElementById('text').value;
        let img_file = document.getElementById('image-upload-btn');
        let video_file = document.getElementById('video-upload-btn');
        let data_img = new FormData();
        data_img.append('text', text);
        
        if (img_file.files && img_file.files[0]) {
            data_img.append('images', img_file.files[0], img_file.files[0].name);
            if ( /\.(jpe?g|png|gif)$/i.test(img_file.files[0].name) === false) { 
                //Validating the Image Type
                alertMessage('bg-danger','image must be jpg/png/gif!', alertMsgAvatar);
                e.preventDefault();
                e.stopPropagation();
                return false;
            } else if (img_file.files[0].size > 1048576) {
                alertMessage('bg-danger','Image file larger than 1MB!', alertMsgAvatar);
                e.preventDefault();
                e.stopPropagation();
                return false;
            }
        }

        if (video_file.files && video_file.files[0]) {
            data_img.append('videos', video_file.files[0], video_file.files[0].name);
            if (/\.(mp4|avi)$/i.test(video_file.files[0].name) === false) {
                alertMessage('bg-danger','image must be mp4/avi!', alertMsgAvatar);
                e.preventDefault();
                e.stopPropagation();
                return false;
            }
        }

        if (text !== '') {
            $.ajax({
                type: "POST",
                beforeSend: function() {
                    spinner.style.visibility = 'visible';
                },   
                url: "/api/user/post/",
                headers: {
                    'X-CSRFToken': csrftoken,
                },
                contentType: false,
                processData: false,
                data: data_img,
                success: function(result) {
                    console.log("result *************", result);
                    // imageTag.src = result['avatar'];
                    result = result['data']
                    user = result['user']
                    document.title = "Post Uploaded";              
                    alertMessage('bg-success','Posted Successfully!', alertMsgAvatar);
                    $('.panel-activity__list').prepend(`
                    <li>
                        <i class="activity__list__icon fa fa-question-circle-o"></i>
                        <div class="activity__list__header d-flex flex-row justify-content-between">
                            <div>
                                <a href="{% if user.email == post.user.email %}{% url 'profile' %}{% else %}{% url 'otherprofile' post.user.email %}{% endif %} ">
                                    <img src="${user['avatar']}" alt="avatar" class="rounded-circle" width="35" height="35" height="35" />
                                    <small class="text-muted">${user['email']}</small>
                                </a>                                      
                            </div>                                
                            <div>
                                <small><span><i class="fa fa-clock"></i> ${result['created_date']}, ${result['created_time']}</span></small> 
                            </div>
                        </div>
                        <div class="activity__list__body entry-content">
                            <p class="text-dark"><strong>${result['text']}</strong></p>
                            ${result['images'] && `<img class="img-responsive img-fluid img-thumbnail p-1" src="${result['images']}" alt="img_post" width="60" />`}
                            ${result['videos'] && `<video poster="" width="450" height="350" controls><source src="${result['videos']}"></video>`}
                        </div>
                        <div class="activity__list__footer">
                            <a href="#"> <i class="fa fa-thumbs-up"></i>0</a>
                            <a href="#"> <i class="fa fa-thumbs-down"></i>0</a>                              
                        </div>                          
                    </li>`);
                    // console.log(input.files[0].size);
                },
                error: function (error) {
                    console.log(error);
                    // console.log(error["responseJSON"]["detail"]);
                    alertMessage('bg-danger','An error occurred!', alertMsgAvatar);
                    if (error.status === 500) alertMessage('bg-danger','Server Error!', alertMsgAvatar);
                },
                complete: function(){
                    spinner.style.visibility = 'hidden';
                },
            });            
        } else {
            alertMessage('bg-danger','TextArea is required', alertMsgAvatar);
        }
        form.reset();        
    }); 
}

// LIKE POST
const LikePost = (id) => {
    let display_like = $(`#display_like-${id}`)
    let thumbs_up = $(`#thumbs-up-${id}`)
    console.log("POST ID:", id)
    $.ajax({
        type: "PUT",
        beforeSend: function() {
            spinner.style.visibility = 'visible';
        },   
        url: "http://127.0.0.1:8000/api/user/like/post/",
        headers: {
            'X-CSRFToken': csrftoken,
        },
        data: JSON.stringify({'post_id': id}),
        success: function(result) {
            console.log(result);
            var has_clicked = result['is_liked']
            display_like.html(result['likes_count']);
            thumbs_up.css('color', has_clicked ? 'rgb(13, 110, 253)' : 'rgb(108, 117, 125)')
            // console.log($(`#thumbs-up-${id}`));
        },
        error: function (error) {
            console.log(error);
            // console.log(error["responseText"]);
            // console.log(error["responseJSON"]["detail"]);
        },
        complete: function(){
            spinner.style.visibility = 'hidden';
        },
        dataType: "json",
        contentType: "application/json"
    });
}

// UNLIKE POST
const UnLikePost = (id) => {
    let display_unlike = $(`#display_unlike-${id}`)
    let thumbs_down = $(`#thumbs-down-${id}`)
    
    $.ajax({
        type: "PUT",
        beforeSend: function() {
            spinner.style.visibility = 'visible';
        },   
        url: "api/user/unlike/post/",
        headers: {
            'X-CSRFToken': csrftoken,
        },
        data: JSON.stringify({'post_id': id}),
        success: function(result) {
            console.log(result);
            display_unlike.html(result['unlikes_count']);
            thumbs_down.css('color', result['is_unliked'] ? 'rgb(13, 110, 253)' : 'rgb(108, 117, 125)')
            // thumbs_up.css('color', result['is_unliked'] && 'rgb(108, 117, 125)')
            // console.log($(`#thumbs-up-${id}`));
        },
        error: function (error) {
            console.log(error);
            // console.log(error["responseText"]);
            // console.log(error["responseJSON"]["detail"]);
        },
        complete: function(){
            spinner.style.visibility = 'hidden';
        },
        dataType: "json",
        contentType: "application/json"
    });
}

// FOLLOW
const FollowUser = (id, id_) => {
    let num_follows = $(`#num-follows-${id}`) 
    let follow_btn = $(`#Follow-btn-${id}`)
    let follow_span = $(`#Follow-btn-${id} span`)
    let follow_modal_row = $('#followermodal .modal-body .row')
    let followmodal_list = $('.followermodal_list')
    let follow_txt = $('#follow_txt')    
    let num_followings = $(`#num-followings-${id}`)

    
    $.ajax({
        type: "PUT",
        beforeSend: function() {
            spinner.style.visibility = 'visible';
        },   
        url: "http://127.0.0.1:8000/api/user/follow/",
        headers: {
            'X-CSRFToken': csrftoken,
        },
        data: JSON.stringify({'user_id': id, 'id_': id_}),
        success: function(result) {
            console.log(result);
            follower = result["follower"]
            following = result["following"]

            num_follows.html(follower['followers_count']);
            follow_btn.css('background', follower["is_followed"] ? 'rgb(32, 35, 36)' : 'rgb(34, 143, 154)')
            follow_span.html(follower["is_followed"] ? 'Following' :  '<i class="fa fa-plus"></i> Follows')
            follow_txt.html(follower["followers"].length > 1 ? 'Followers' : 'Follower')

            if (follower["followers"].length === 0) {
                    follow_modal_row.html('<h3 class="text-center"><strong>No Follower Yet!</strong></h3>')
                } else {
                    followmodal_list.append(
                        follower["followers"].forEach(follower => {
                            
                            `<li>                                
                                <i class="activity__list__icon fa fa-question-circle-o"></i>
                                <div class="activity__list__header d-flex flex-row justify-content-between">
                                    <div>
                                        <a href= "{% if user.email == ${follower.email} %}{% url 'profile' %}{% else %}{% url 'otherprofile' ${follower.email} %}{% endif %} ">
                                            <img src=${follower.avatar ? follower.avatar : `static/default.png`} alt="avatar" class="rounded-circle" width="35" height="35" />
                                            <div class="d-flex flex-column">
                                                <small class="text-muted">${follower.first_name} ${follower.last_name}</small>
                                                <small class="text-muted">${follower.email}</small>
                                            </div>                                            
                                        </a>                                      
                                    </div>
                                </div>                        
                            </li>`
                        }
                ));  
            }
            
            
            

            // thumbs_up.css('color', result['is_unliked'] && 'rgb(108, 117, 125)')
            // console.log($(`#thumbs-up-${id}`));
        },
        error: function (error) {
            console.log(error);
            // console.log(error["responseText"]);
            // console.log(error["responseJSON"]["detail"]);
        },
        complete: function(){
            spinner.style.visibility = 'hidden';
        },
        dataType: "json",
        contentType: "application/json"
    });
}