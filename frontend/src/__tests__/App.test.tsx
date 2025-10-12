import { render, screen } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

import App from "../App";

const queryClient = new QueryClient();

const renderApp = () =>
  render(
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  );

describe("App", () => {
  it("renders form heading", () => {
    renderApp();
    // Use getByRole to find the main heading instead of multiple LGBTQ+ texts
    expect(screen.getByRole("heading", { name: /เครื่องมือวิเคราะห์ความหลากหลายทางเพศ LGBTQ\+/i })).toBeInTheDocument();
  });
});
