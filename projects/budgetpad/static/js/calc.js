"use strict";

const input = document.querySelector("input");

function calc(number) {
  input.value = input.value + number;
}

function result() {
  try {
    input.value = eval(input.value);
  } catch (err) {
    alert("Please Enter a valid number");
  }
}

function clears() {
  input.value = "";
}

function del() {
  input.value = input.value.slice(0, -1);
}
