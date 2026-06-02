import { Sidebar } from "./Sidebar";
import { StatusBar } from "./StatusBar";

type LayoutProps = {
  children: React.ReactNode;
};

export function Layout({ children }: LayoutProps) {
  return (
    <div className="shell">
      <Sidebar />
      <main className="content">{children}</main>
      <StatusBar />
    </div>
  );
}
