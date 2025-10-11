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
    expect(screen.getByText(/lgbtq\+/i)).toBeInTheDocument();
  });
});
