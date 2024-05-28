import { postDataPromise } from "./ApiService";

export const sendUserMessage = async (params) => {
  return postDataPromise(`chat`, params);
};

export const startTrainBot = async () => {
  return postDataPromise(`train`);
}

export const clearData = async () => {
  return postDataPromise(`clear`);
}
