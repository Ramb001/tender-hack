import { baseApi } from "@/shared/api";
import { combineReducers } from "@reduxjs/toolkit";

export const rootReducer = combineReducers({
  [baseApi.reducerPath]: baseApi.reducer,
});
