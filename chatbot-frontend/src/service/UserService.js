import { getDataPromise, postDataPromise } from "./ApiService";

export const getUsername = async () => {
  return getDataPromise(`username`);
};

export const changeName = async (name) => {
  return postDataPromise(`username`, name);
};
