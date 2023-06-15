function checkInput() {
  let input = document.getElementById("myInput");
  if (input.value !== "") {
    input.classList.add("filled");
  } else {
    input.classList.remove("filled");
  }
}
