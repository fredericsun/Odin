import { render, screen } from "@testing-library/react";
import { test, expect } from "vitest";

import Page from "../src/app/page";

test("shows alerts heading", () => {
  render(<Page />);
  expect(screen.getByText("Alerts")).toBeInTheDocument();
});
