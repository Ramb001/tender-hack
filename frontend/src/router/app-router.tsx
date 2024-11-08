import { Layout } from "@/components/layout";
import { MainPage } from "@/pages/main";
import { Routes } from "@/shared/consts";
import { createBrowserRouter } from "react-router-dom";

export const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      {
        element: <MainPage />,
        path: Routes.main,
      },
    ],
  },
]);
