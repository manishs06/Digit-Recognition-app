# 🚀 Vercel Deployment Guide

This guide will help you deploy your AI Digit Recognition app to Vercel in minutes!

## 📋 Prerequisites

- A [Vercel account](https://vercel.com/signup) (free tier works great!)
- Your code pushed to GitHub (which you're about to do!)
- The Vercel CLI (optional, but recommended)

## 🎯 Quick Deploy (Recommended)

### Method 1: Deploy via Vercel Dashboard (Easiest)

1. **Push your code to GitHub** (already done! ✅)

2. **Go to [Vercel Dashboard](https://vercel.com/new)**

3. **Import your GitHub repository**
   - Click "Import Project"
   - Select "Import Git Repository"
   - Choose `manishs06/Digit-Recognition-app`

4. **Configure the project**
   - Framework Preset: **Other**
   - Root Directory: `./` (leave as default)
   - Build Command: (leave empty)
   - Output Directory: `public`

5. **Click "Deploy"** 🎉

That's it! Vercel will automatically:
- Detect the `vercel.json` configuration
- Build your serverless functions
- Deploy your static assets
- Give you a live URL!

### Method 2: Deploy via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy from your project directory**
   ```bash
   cd Digit-Recognition
   vercel
   ```

4. **Follow the prompts**
   - Link to existing project? **No**
   - Project name: **digit-recognition-app**
   - Directory: **./** (current directory)
   - Override settings? **No**

5. **Deploy to production**
   ```bash
   vercel --prod
   ```

## 📁 Project Structure for Vercel

```
Digit-Recognition-app/
├── api/
│   └── predict.py          # Serverless function for predictions
├── public/
│   └── index.html          # Main HTML page
├── static/
│   ├── style.css           # Styles
│   └── script.js           # JavaScript
├── model.h5                # TensorFlow model (⚠️ see note below)
├── requirements.txt        # Python dependencies
├── vercel.json            # Vercel configuration
└── .vercelignore          # Files to exclude from deployment
```

## ⚠️ Important: Model File Size

The `model.h5` file (~1.4 MB) should work fine with Vercel's limits. However, if you encounter issues:

### Option 1: Use Vercel's File Size Limits
- Free tier: 100 MB per deployment
- Your model is only 1.4 MB, so you're good! ✅

### Option 2: Host Model Externally (if needed)
If you need to use a larger model in the future:

1. Upload `model.h5` to cloud storage (AWS S3, Google Cloud Storage, etc.)
2. Update `api/predict.py` to download the model on first request
3. Cache it in `/tmp` directory

## 🔧 Environment Variables (Optional)

If you need to add environment variables:

1. Go to your project in Vercel Dashboard
2. Navigate to **Settings** → **Environment Variables**
3. Add any required variables

For this project, no environment variables are needed! 🎉

## 🌐 Custom Domain (Optional)

Want a custom domain like `digit-ai.yourdomain.com`?

1. Go to **Settings** → **Domains**
2. Add your custom domain
3. Follow DNS configuration instructions
4. Done! 🎊

## 🔍 Troubleshooting

### Issue: "Module not found" error

**Solution**: Make sure `requirements.txt` includes all dependencies:
```txt
tensorflow
Flask
numpy
pillow
```

### Issue: "Function timeout"

**Solution**: Vercel free tier has a 10-second timeout. The model prediction is fast (<1s), so this shouldn't be an issue.

### Issue: "Build failed"

**Solution**: Check the build logs in Vercel dashboard. Common fixes:
- Ensure `vercel.json` is in the root directory
- Verify all file paths are correct
- Check that `model.h5` is committed to the repo

### Issue: Static files not loading

**Solution**: Ensure your `vercel.json` routes are correct:
```json
{
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    }
  ]
}
```

## 📊 Performance Tips

1. **Cold Starts**: First request might be slower (~2-3s) due to model loading. Subsequent requests are fast!

2. **Optimize Model**: If you need faster cold starts, consider:
   - Using TensorFlow Lite
   - Quantizing the model
   - Using a smaller architecture

3. **Caching**: Vercel automatically caches static assets (CSS, JS)

## 🔄 Continuous Deployment

Once connected to GitHub, Vercel automatically deploys:
- **Production**: Every push to `main` branch
- **Preview**: Every pull request

You can disable this in **Settings** → **Git** if needed.

## 📱 Testing Your Deployment

After deployment, test these features:

1. ✅ Page loads correctly
2. ✅ Canvas drawing works
3. ✅ Prediction API responds
4. ✅ Confidence scores display
5. ✅ Mobile responsiveness
6. ✅ All animations work

## 🎨 Post-Deployment

Your app will be live at:
```
https://your-project-name.vercel.app
```

Share it with the world! 🌍

### Update README with Live Link

Add this badge to your README:
```markdown
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/manishs06/Digit-Recognition-app)

🔗 **Live Demo**: [https://your-app.vercel.app](https://your-app.vercel.app)
```

## 🆘 Need Help?

- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Community](https://github.com/vercel/vercel/discussions)
- [Python on Vercel](https://vercel.com/docs/functions/serverless-functions/runtimes/python)

## 🎉 Success!

Your AI Digit Recognition app is now live on Vercel! 

**Next Steps:**
- Share your app URL
- Add it to your portfolio
- Tweet about it with #BuiltWithVercel
- Keep building amazing things! 🚀

---

**Built with ❤️ using TensorFlow, Flask & Vercel**
