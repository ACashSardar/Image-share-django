var inputImg = document.querySelector("#inputImg");
var img = document.querySelector("#displayImg");
var fullImgBox = document.getElementById("full-img-box");
var fullImg = document.getElementById("fullImg");
var img_capt = document.getElementById("img-capt");
var selCat = document.querySelector("#cat-items");
var signUpFieldName = document.querySelectorAll(".signup-field-name");

// console.log("SignUP field Name=", signUpFieldName);
Array.from(signUpFieldName).forEach((elem) => {
  console.log(elem.innerHTML);
  if (elem.innerHTML == "password1") elem.innerHTML = "Password";
  else if (elem.innerHTML == "password2") elem.innerHTML = "Confirm password";
  else if (elem.innerHTML == "username") elem.innerHTML = "Username";
});

inputImg.addEventListener("change", function () {
  const file = this.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = function () {
      const result = reader.result;
      img.src = result;
      console.log(result);
    };
    reader.readAsDataURL(file);
  }
});

function openFullImg(pic, imgCapt, imgURL) {
  console.log(fullImgBox);
  fullImgBox.style.display = "flex";
  fullImg.src = pic;
  img_capt.innerHTML = imgCapt;
  console.log(fullImgBox.style.display, imgCapt);
  console.log(imgCapt, imgURL);
}

function closeImg() {
  fullImgBox.style.display = "none";
}

function downloadImg() {
  console.log(fullImg);
  var a = document.createElement("a");
  a.href = fullImg.src;
  a.download = "output.png";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}
