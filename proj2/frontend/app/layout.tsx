import "../styles/globals.css";
import LayoutWrapper from "./components/LayoutWrapper";

export const metadata = {
  title: "Movie Munchers",
  description: "Snacks for every movie night",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-white text-gray-900 flex flex-col">
        <LayoutWrapper>{children}</LayoutWrapper>
      </body>
    </html>
  );
}
