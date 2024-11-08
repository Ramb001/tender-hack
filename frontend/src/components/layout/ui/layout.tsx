import { Footer } from "@/components/footer";
import { Header } from "@/components/header";
import { Outlet } from "react-router-dom";

export const Layout = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <main className="flex-grow max-w-[1300px] mx-[auto] w-full">
        <Outlet />
      </main>
      <Footer />
    </div>
  );
};
