import fetchApi from "./Axios";
import axios from "axios";

axios.defaults.headers.common["Content-Type"] = "application/json";

export async function getData(endpoint, queryParams = {}) {
  let jsonData = [];
  try {
    const response = await fetchApi.get(
      document.getElementById("root").baseURI + endpoint,
      { params: queryParams }
    );
    if (![200, 201].includes(response.status)) throw await response.text();
    jsonData = await response.data;
  } catch (error) {
    console.log(error);
  }
  return jsonData;
}

export async function postData(endpoint, postData) {
  let jsonData = [];
  try {
    const { data } = await fetchApi.post(
      document.getElementById("root").baseURI + endpoint,
      postData
    );
    jsonData = await data;
  } catch (error) {
    return error;
  }
  return jsonData;
}

export async function deleteData(endpoint, queryParams = {}) {
  let jsonData = [];
  try {
    const { data } = await fetchApi.delete(
      document.getElementById("root").baseURI + endpoint,
      { params: queryParams }
    );
    jsonData = await data;
  } catch (error) {
    console.log(error);
  }
  return jsonData;
}

export async function putData(endpoint, putData, queryParams = {}) {
  let jsonData = [];
  try {
    const { data } = await fetchApi.put(
      document.getElementById("root").baseURI + endpoint,
      putData,
      { params: queryParams }
    );
    jsonData = await data;
  } catch (error) {
    return error;
  }
  return jsonData;
}

export async function getDataPromise(endpoint, queryParams = {}) {
  return fetchApi.get(endpoint, {
    params: queryParams,
  });
}

export async function postDataPromise(endpoint, postData) {
  return fetchApi.post(endpoint, postData);
}

export async function deleteDataPromise(endpoint, queryParams = {}) {
  return fetchApi.delete(endpoint, {
    params: queryParams,
  });
}

export async function putDataPromise(endpoint, data) {
  return fetchApi.put(endpoint, data);
}
