// Custom magic-link email — branded with the Supernova palette so the
// inbox preview reads on-brand instead of the default Auth.js plaintext.

import { Resend } from "resend";

type Args = {
  to: string;
  url: string;
  from: string;
  resendApiKey: string;
};

export async function sendMagicLinkEmail({
  to,
  url,
  from,
  resendApiKey,
}: Args) {
  const resend = new Resend(resendApiKey);
  const { error } = await resend.emails.send({
    from,
    to,
    subject: "✨ Masuk ke Supernova",
    html: html(url),
    text: text(url),
  });
  if (error) {
    throw new Error(`Resend error: ${error.message ?? JSON.stringify(error)}`);
  }
}

function html(url: string) {
  // Inline styles only — most email clients strip <style>.
  return /* html */ `
<!doctype html>
<html lang="id">
  <body style="margin:0;padding:0;background:#0E1226;font-family:-apple-system,'Segoe UI',Inter,sans-serif;color:#F2EAD3;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="padding:40px 16px;">
      <tr>
        <td align="center">
          <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width:480px;background:#181C36;border-radius:16px;padding:32px;">
            <tr>
              <td style="font-family:Georgia,serif;font-size:28px;font-weight:600;color:#E9C77B;text-align:center;padding-bottom:8px;">
                ✨ Supernova
              </td>
            </tr>
            <tr>
              <td style="font-size:14px;color:#9AA3B5;text-align:center;padding-bottom:32px;">
                Klik tombol di bawah buat masuk. Tautan ini cuma berlaku 15 menit dan cuma bisa dipake sekali.
              </td>
            </tr>
            <tr>
              <td align="center" style="padding-bottom:32px;">
                <a href="${url}" style="display:inline-block;background:#E9C77B;color:#0E1226;padding:14px 32px;border-radius:10px;text-decoration:none;font-weight:600;font-size:15px;">
                  Masuk ke Supernova
                </a>
              </td>
            </tr>
            <tr>
              <td style="font-size:12px;color:#6F7891;text-align:center;line-height:1.5;">
                Kalau tombolnya gak jalan, salin link ini ke browser:<br />
                <span style="color:#9AA3B5;word-break:break-all;">${url}</span>
              </td>
            </tr>
          </table>
          <div style="margin-top:24px;font-size:11px;color:#6F7891;">
            Kalau lo gak nge-request ini, abaikan aja. Akun lo tetap aman.
          </div>
        </td>
      </tr>
    </table>
  </body>
</html>`.trim();
}

function text(url: string) {
  return [
    "✨ Supernova",
    "",
    "Klik link di bawah buat masuk (berlaku 15 menit, sekali pakai):",
    url,
    "",
    "Kalau lo gak nge-request, abaikan aja.",
  ].join("\n");
}
