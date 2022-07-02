var inputImg = document.querySelector("#inputImg");
var img = document.querySelector("#displayImg");
var fullImgBox = document.getElementById("full-img-box");
var fullImg = document.getElementById("fullImg");
var img_capt = document.getElementById("img-capt");
var selCat = document.querySelector("#cat-items");
var signUpFieldName = document.querySelectorAll(".signup-field-name");
var MyPost = document.querySelectorAll(".homepageImgs");
var LoadMoreBtn = document.getElementById("load-more");
var currentPosts = 5;

Array.from(signUpFieldName).forEach((elem) => {
  console.log(elem.innerHTML);
  if (elem.innerHTML == "password1") elem.innerHTML = "Password";
  else if (elem.innerHTML == "password2") elem.innerHTML = "Confirm password";
  else if (elem.innerHTML == "username") elem.innerHTML = "Username";
});

if (LoadMoreBtn) {
  let i = 0;
  MyPost.forEach((elem) => {
    if (i > currentPosts) elem.style.display = "none";
    i++;
  });
  if (MyPost.length < 12) {
    LoadMoreBtn.style.display = "none";
  }

  LoadMoreBtn.addEventListener("click", () => {
    for (let i = currentPosts; i <= currentPosts + 6; i++) {
      if (MyPost[i]) {
        console.log(MyPost[i].style.display);
        MyPost[i].style.display = "block";
      } else {
        LoadMoreBtn.style.display = "none";
      }
    }
    currentPosts += 6;
  });
}

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
  let a = document.createElement("a");
  a.href = fullImg.src;
  a.download = "output.png";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}
