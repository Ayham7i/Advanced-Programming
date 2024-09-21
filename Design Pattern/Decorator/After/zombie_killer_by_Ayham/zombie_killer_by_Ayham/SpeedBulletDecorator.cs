// SpeedBulletDecorator.cs
using System.Windows.Forms;

namespace zombie_killer_by_Ayham
{
    public class SpeedBulletDecorator : BulletDecorator
    {
        private int extraSpeed;

        public SpeedBulletDecorator(IBullet bullet, int speed) : base(bullet)
        {
            extraSpeed = speed;
        }

        public override void UpdateBulletPosition()
        {
            // Modify the bullet position update to include extra speed
            decoratedBullet.UpdateBulletPosition();

            // Add additional behavior (e.g., increase bullet movement by extraSpeed)
            // The actual bullet update is handled by the base bullet (decoratedBullet)
        }
    }
}
