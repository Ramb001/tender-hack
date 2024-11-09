import { FooterNavLinks } from "../model/footer-items";
import { FooterSocialLinks } from "../model/footer-items";

export const Footer = () => {
  return (
    <footer className="bg-gray-100 px-8 shadow-inner py-6">
      <div className="container mx-auto flex flex-col items-center space-y-4 sm:flex-row sm:justify-between sm:space-y-0">
        {/* Left Side: Navigation Links */}
        <nav className="flex   text-gray-700">
          {FooterNavLinks.map((item) => (
            <a
              key={item.href}
              href={item.href}
              className="text-pale-black hover:text-main-blue transition-colors duration-300"
            >
              {item.value}
            </a>
          ))}
        </nav>

        {/* Right Side: Social Media Icons (or placeholder links) */}
        <div className="flex space-x-4 text-gray-700">
          {FooterSocialLinks.map((item) => (
            <a key={item.href} href={item.href}>
              {item.icon && (
                <item.icon className="size-6 stroke-pale-black hover:stroke-main-blue transition-colors duration-300" />
              )}
            </a>
          ))}
        </div>
      </div>
    </footer>
  );
};
