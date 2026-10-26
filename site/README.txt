HOMESTAY STARTER WEBSITE - HOW TO USE

1. PHOTOS: put the client's photos in the images/ folder with these names (jpg):
   hero.jpg, about.jpg, room-1.jpg, room-2.jpg, room-3.jpg, gallery-1.jpg ... gallery-12.jpg
   (Until a photo exists, a dark gradient shows instead. Keep each photo under 300 KB for fast loading.)

2. DETAILS: open build.py in any text editor. Change the CONFIG block at the top
   (name, phone, WhatsApp number, email, address, social links, site URL),
   plus ROOMS, REVIEWS and AMENITIES just below it.
   WhatsApp number format: country code + number, no + or spaces (e.g. 919876543210).

3. REBUILD: run   python3 build.py   (it regenerates all 5 HTML pages).

4. REVIEWS: the sample reviews are placeholders. Replace them with the client's REAL reviews before launch.

5. DEPLOY: upload the whole folder (except build.py if you like) to Netlify, Vercel, Cloudflare Pages
   or any hosting. No build step needed on the host.

6. ENQUIRY FORM: sends the enquiry to the client's WhatsApp, so no backend is needed.
