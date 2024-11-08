import { HeaderItems } from "../model/header-items";

export const Header = () => {
  return (

    <header className="bg-white shadow-md p-4 flex items-start">
      <nav className="flex justify-center space-x-8">

   
        {HeaderItems.map((item) => (
          <a
            key={item.href}
            href={item.href}
            className="text-pale-black hover:text-main-blue transition-colors duration-300"
          >
            {item.value}
          </a>
        ))}
      </nav>
    </header>
  );
};
