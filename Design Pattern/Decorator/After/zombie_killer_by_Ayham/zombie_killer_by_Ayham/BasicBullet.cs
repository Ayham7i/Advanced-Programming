// BasicBullet.cs
using System;
using System.Drawing;
using System.Windows.Forms;

namespace zombie_killer_by_Ayham
{
    public class BasicBullet : IBullet
    {
        public string Direction { get; set; }
        public int BulletLeft { get; set; }
        public int BulletTop { get; set; }

        private int speed = 20;
        private PictureBox bullet = new PictureBox();
        private Timer bulletTimer = new Timer();

        public BasicBullet(string direction, int left, int top)
        {
            Direction = direction;
            BulletLeft = left;
            BulletTop = top;
        }

        public void MakeBullet(Form form)
        {
            bullet.BackColor = Color.BurlyWood;
            bullet.Size = new Size(10, 10);
            bullet.Tag = "bullet";
            bullet.Left = BulletLeft;
            bullet.Top = BulletTop;
            bullet.BringToFront();
            form.Controls.Add(bullet);

            bulletTimer.Interval = speed;
            bulletTimer.Tick += new EventHandler(BulletTimerEvent);
            bulletTimer.Start();
        }

        private void BulletTimerEvent(object sender, EventArgs e)
        {
            UpdateBulletPosition();
            if (bullet.Left < 10 || bullet.Left > 860 || bullet.Top < 10 || bullet.Top > 600)
            {
                bulletTimer.Stop();
                bulletTimer.Dispose();
                bullet.Dispose();
                bulletTimer = null;
                bullet = null;
            }
        }

        public void UpdateBulletPosition()
        {
            if (Direction == "left")
            {
                bullet.Left -= speed;
            }
            else if (Direction == "right")
            {
                bullet.Left += speed;
            }
            else if (Direction == "up")
            {
                bullet.Top -= speed;
            }
            else if (Direction == "down")
            {
                bullet.Top += speed;
            }
        }
    }
}
