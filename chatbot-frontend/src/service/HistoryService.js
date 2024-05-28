import { getDataPromise, postDataPromise, putDataPromise } from "./ApiService";

export const addHistoryToDb = async (history) => {
  return postDataPromise(`history`, history);
};

export const getHistoryByIdFromDb = async (id) => {
  return getDataPromise(`history/${id}`);
};

export const getAllHistoriesFromDb = async () => {
  return getDataPromise(`histories`);
};

export const deleteHistoryFromDb = async (id) => {
  return postDataPromise(`delete_history`, id);
};

export const updateHistoryInDb = async (params) => {
  return putDataPromise(`history`, params);
};
