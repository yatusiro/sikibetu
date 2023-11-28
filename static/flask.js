var nowuser = null;

//登出
// localStorage.removeItem('loggedInUser');
//获取
//let loggedInUser = localStorage.getItem('loggedInUser');
function testflask3() {
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;

    $.ajax({
        url: '/login_action',
        type: 'POST',
        data: {
            "username": username,
            "password": password
        },
        dataType: 'json',
        success: function(response) {
            if (response.status === 'success') {
                // 将账号保存到localStorage
                localStorage.setItem('loggedInUser', username);

                // 根据用户信息是否存在来决定跳转的页面
                if (response.infoExists==false) {
                    window.location.href = '/mainpage';
                } else {
                    window.location.href = '/main';
                }
            } else {
                alert('登录失败！');
            }
        }
    });
}


function registerUser() {
    let mail = document.getElementById('mail').value;
    let phonenumber = document.getElementById('phonenumber').value;
    let password = document.getElementById('reg_password').value;

    $.ajax({
        url: '/register_action',
        type: 'POST',
        data: {
            "mail": mail,
            "phonenumber": phonenumber,
            "password": password
        },
        dataType: 'json',
        success: function(response) {
            console.log(response);
            // 这里可以进一步处理服务器的响应
            // 例如：显示一个消息给用户或者更新页面的其他部分
            window.location.href = '/';  // 可以选择在成功后跳回登录页面
        }
    });
}

function saveUserInfo() {
    let mail = localStorage.getItem('loggedInUser');
    let gender = document.getElementById('gender').value;
    let birthdate = document.getElementById('birthdate').value;
    let weight = document.getElementById('weight').value;

    $.ajax({
        url: '/save_user_info',
        type: 'POST',
        data: {
            "mail": mail,
            "gender": gender,
            "birthdate": birthdate,
            "weight": weight
        },
        dataType: 'json',
        success: function(response) {
            alert(response.message);
            window.location.href = '/main';
        }
    });
}
